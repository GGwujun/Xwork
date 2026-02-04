from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.schemas import OpenSpec, Requirement
from app.logger import setup_logging, attach_request_id
from app.exceptions import register_exception_handlers
from app.agent_swarm import agent_swarm
from app.context_server import context_server
from app.opencode_integration import get_opencode_generator, OpenCodeError
from app.tfs_mcp import mcp_list_work_items, mcp_get_work_item, mcp_create_work_item, mcp_trigger_build
from app.checkin_guard import validate_before_checkin
from app.session_sync import save_current_session, get_share_link, session_sync
import uuid

setup_logging()
app = FastAPI(title="Enterprise Forge Engine")
attach_request_id(app)
register_exception_handlers(app)

# Configure CORS for Tauri/Web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Enterprise Forge Engine is running", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/opencode/status")
async def opencode_status():
    """
    获取OpenCode服务状态

    Returns:
        OpenCode服务信息，包括URL、运行状态等
    """
    try:
        from app.openwork_bridge import get_openwork_bridge
        bridge = get_openwork_bridge()
        service_info = bridge.get_service_info()

        if service_info:
            return {
                "status": "connected",
                "source": "openwork",
                "service_info": service_info
            }
        else:
            # 尝试使用环境变量或默认配置
            import os
            opencode_url = os.getenv('OPENCODE_URL', 'http://127.0.0.1:4096')
            return {
                "status": "configured",
                "source": "environment",
                "opencode_url": opencode_url,
                "message": "OpenWork未运行，使用配置的URL"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# --- Spec Generation ---

@app.post("/spec/generate", response_model=OpenSpec)
async def generate_spec(requirement: Requirement, workspace_path: Optional[str] = None):
    """
    Generate OpenSpec using Agent Swarm (PM + Architect).

    Args:
        requirement: 需求信息
        workspace_path: 目标工作区路径（可选）
    """
    try:
        spec = await agent_swarm.generate_spec(requirement, workspace_path)
        return spec
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to generate spec: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate spec: {str(e)}")


class GenerateViaOpenCodeBody(BaseModel):
    requirement: Requirement
    workspace_path: Optional[str] = None
    opencode_url: Optional[str] = None


@app.post("/spec/generate-via-opencode", response_model=OpenSpec)
async def generate_spec_via_opencode(body: GenerateViaOpenCodeBody):
    """
    Generate OpenSpec using OpenCode engine directly.

    This endpoint creates a temporary OpenCode session, sends a specialized prompt,
    and parses the response into OpenSpec format.

    Args:
        body: Request body containing requirement, workspace_path, and opencode_url
    """
    try:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Starting OpenCode spec generation for: {body.requirement.summary}")

        # 获取OpenCode生成器实例
        # 优先级：请求参数 > OpenWork桥接 > 默认值
        opencode_url = body.opencode_url
        if not opencode_url:
            try:
                from app.openwork_bridge import get_openwork_bridge
                bridge = get_openwork_bridge()
                opencode_url = bridge.get_opencode_url()
                if opencode_url:
                    logger.info(f"从OpenWork获取到OpenCode URL: {opencode_url}")
            except Exception as e:
                logger.debug(f"无法从OpenWork获取URL: {str(e)}")

        # 如果仍然没有URL，使用默认值
        if not opencode_url:
            opencode_url = "http://127.0.0.1:4096"
            logger.warning(f"使用默认OpenCode URL: {opencode_url}")

        generator = get_opencode_generator(opencode_url)

        # 生成规范
        spec = await generator.generate_spec(
            requirement=body.requirement,
            workspace_path=body.workspace_path
        )

        logger.info(f"Successfully generated OpenSpec via OpenCode: {spec.project_name}")
        return spec

    except OpenCodeError as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"OpenCode generation failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"OpenCode服务错误: {str(e)}"
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in OpenCode generation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"生成规范时发生未知错误: {str(e)}"
        )

# --- Skills & Context ---

@app.get("/skills")
async def list_skills():
    skills = context_server.skills_loader.list_skills()
    return [skill.model_dump() for skill in skills]

@app.get("/skills/{name}")
async def get_skill(name: str):
    skill = context_server.skills_loader.get_skill(name)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.model_dump()

@app.post("/skills/reload")
async def reload_skills():
    skills = context_server.skills_loader.reload()
    return {"count": len(skills)}

class SkillsSearchBody(BaseModel):
    query: str
    tags: List[str] = []
    top_k: int = 5

@app.post("/skills/search")
async def search_skills(body: SkillsSearchBody):
    results = context_server.retrieve_skills(body.query, tags=body.tags, top_k=body.top_k)
    return [
        {
            "skill": skill.model_dump(),
            "score": score,
        }
        for skill, score in results
    ]

class ContextBuildBody(BaseModel):
    query: str
    tags: List[str] = []
    top_k: int = 5
    max_tokens: int = 2000
    model_name: Optional[str] = None

@app.post("/context/build")
async def build_context(body: ContextBuildBody):
    context, skills = context_server.build_skills_context(
        body.query,
        tags=body.tags,
        top_k=body.top_k,
        max_tokens=body.max_tokens,
        model_name=body.model_name,
    )
    return {"context": context, "skills": skills}

# --- TFS / Azure DevOps Integration ---

@app.get("/tfs/workitems")
async def list_work_items(project: str = "WINNING-6.0", item_type: Optional[str] = None):
    """List work items from TFS."""
    return await mcp_list_work_items(project, item_type)

@app.get("/tfs/workitems/{item_id}")
async def get_work_item(item_id: int):
    """Get a specific work item."""
    item = await mcp_get_work_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Work item not found")
    return item

class CreateWorkItemBody(BaseModel):
    project: str
    type: str
    title: str
    description: str = ""
    assigned_to: str = ""

@app.post("/tfs/workitems")
async def create_work_item(body: CreateWorkItemBody):
    """Create a new work item in TFS."""
    return await mcp_create_work_item(
        project=body.project,
        item_type=body.type,
        title=body.title,
        description=body.description,
        assigned_to=body.assigned_to,
    )

@app.post("/tfs/build")
async def trigger_build(project: str, pipeline_id: int):
    """Trigger a CI/CD pipeline."""
    return await mcp_trigger_build(project, pipeline_id)

# --- TFS Authentication ---

from app.tfs_auth import login_with_pat, get_oauth_url, oauth_callback, check_auth_status, logout as tfs_logout

class TfsLoginBody(BaseModel):
    organization: str
    pat: str

@app.post("/tfs/auth/login")
async def tfs_login(body: TfsLoginBody):
    """Login to TFS using PAT."""
    return await login_with_pat(body.organization, body.pat)

@app.get("/tfs/auth/oauth/url")
async def tfs_oauth_url(organization: str):
    """Get OAuth authorization URL."""
    return await get_oauth_url(organization)

@app.get("/tfs/auth/oauth/callback")
async def tfs_oauth_callback(code: str, state: str = ""):
    """Handle OAuth callback."""
    return await oauth_callback(code, state)

@app.get("/tfs/auth/status")
async def tfs_auth_status():
    """Check TFS authentication status."""
    return await check_auth_status()

@app.post("/tfs/auth/logout")
async def tfs_logout_endpoint():
    """Logout from TFS."""
    return await tfs_logout()

# --- Check-in Guard ---

@app.post("/checkin/validate")
async def validate_checkin(project_root: str):
    """Run pre-commit checks before TFS check-in."""
    return await validate_before_checkin(project_root)

# --- Session Sync ---

class SaveSessionBody(BaseModel):
    session_id: str
    user_id: str
    project_name: str
    messages: List[Dict[str, Any]]
    spec: Optional[Dict[str, Any]] = None
    file_changes: List[str] = []

@app.post("/session/save")
async def save_session(body: SaveSessionBody):
    """Save session state for collaboration."""
    session_id = await save_current_session(
        session_id=body.session_id,
        user_id=body.user_id,
        project_name=body.project_name,
        messages=body.messages,
        spec=body.spec,
        file_changes=body.file_changes,
    )
    return {"session_id": session_id, "status": "saved"}

@app.get("/session/{session_id}")
async def load_session(session_id: str):
    """Load a session by ID."""
    session = await session_sync.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()

@app.post("/session/{session_id}/share")
async def share_session(session_id: str):
    """Generate a shareable link for a session."""
    try:
        link = await get_share_link(session_id)
        return {"share_link": link}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- Editor IPC (VS Code Integration) ---

from app.editor_ipc import open_in_vscode, apply_edits, editor_ipc
from app.spec_versioning import SpecVersion
from app.spec_lifecycle import SpecLifecycle, SpecStatus

# 初始化版本管理和生命周期管理
spec_version = SpecVersion()
spec_lifecycle = SpecLifecycle()

@app.get("/editor/status")
async def editor_status():
    """Check if VS Code is available."""
    return {"available": editor_ipc.is_available()}

@app.post("/editor/open")
async def open_file_in_editor(file_path: str, line: Optional[int] = None):
    """Open a file in VS Code."""
    return await open_in_vscode(file_path, line)

class ApplyEditsBody(BaseModel):
    edits: List[Dict[str, Any]]

@app.post("/editor/apply")
async def apply_file_edits(body: ApplyEditsBody):
    """Apply file edits (from AI-generated changes)."""
    return await apply_edits(body.edits)

# --- OpenSpec Versioning & Lifecycle ---

@app.get("/spec/{requirement_id}/versions")
async def list_spec_versions(requirement_id: str):
    """列出 OpenSpec 的所有版本"""
    versions = spec_version.list_versions(requirement_id)
    return {"versions": [v.dict() for v in versions]}

@app.get("/spec/{requirement_id}/version/{version}")
async def get_spec_version(requirement_id: str, version: int):
    """获取指定版本的 OpenSpec"""
    spec_data = spec_version.get_version(requirement_id, version)
    if spec_data is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return spec_data

@app.get("/spec/{requirement_id}/version/latest")
async def get_latest_spec_version(requirement_id: str):
    """获取最新版本的 OpenSpec"""
    spec_data = spec_version.get_latest_version(requirement_id)
    if spec_data is None:
        raise HTTPException(status_code=404, detail="No version found")
    return spec_data

class CompareVersionsBody(BaseModel):
    version1: int
    version2: int

@app.post("/spec/{requirement_id}/compare")
async def compare_spec_versions(requirement_id: str, body: CompareVersionsBody):
    """比较两个版本的差异"""
    diff = spec_version.compare_versions(requirement_id, body.version1, body.version2)
    return diff

class RollbackBody(BaseModel):
    version: int

@app.post("/spec/{requirement_id}/rollback")
async def rollback_spec_version(requirement_id: str, body: RollbackBody):
    """回滚到指定版本"""
    success = spec_version.rollback_to_version(requirement_id, body.version)
    if not success:
        raise HTTPException(status_code=400, detail="Rollback failed")
    return {"status": "success", "version": body.version}

@app.get("/spec/{requirement_id}/lifecycle")
async def get_spec_lifecycle(requirement_id: str):
    """获取 OpenSpec 生命周期信息"""
    lifecycle_info = spec_lifecycle.get_lifecycle_info(requirement_id)
    return lifecycle_info

@app.get("/spec/{requirement_id}/status")
async def get_spec_status(requirement_id: str):
    """获取 OpenSpec 当前状态"""
    status = spec_lifecycle.get_status(requirement_id)
    return {"status": status.value}

class SubmitReviewBody(BaseModel):
    submitter: str
    reason: str = ""

@app.post("/spec/{requirement_id}/submit")
async def submit_spec_for_review(requirement_id: str, body: SubmitReviewBody):
    """提交 OpenSpec 审批"""
    success = spec_lifecycle.submit_for_review(
        requirement_id=requirement_id,
        submitter=body.submitter,
        reason=body.reason
    )
    if not success:
        raise HTTPException(status_code=400, detail="Cannot submit for review")
    return {"status": "success", "new_status": SpecStatus.REVIEW.value}

class ApproveBody(BaseModel):
    approver: str
    spec_data: Dict[str, Any]
    reason: str = ""

@app.post("/spec/{requirement_id}/approve")
async def approve_spec(requirement_id: str, body: ApproveBody):
    """审批通过 OpenSpec"""
    success = spec_lifecycle.approve(
        requirement_id=requirement_id,
        approver=body.approver,
        spec_data=body.spec_data,
        reason=body.reason
    )
    if not success:
        raise HTTPException(status_code=400, detail="Cannot approve")
    return {"status": "success", "new_status": SpecStatus.APPROVED.value}

class RejectBody(BaseModel):
    approver: str
    reason: str

@app.post("/spec/{requirement_id}/reject")
async def reject_spec(requirement_id: str, body: RejectBody):
    """审批退回 OpenSpec"""
    success = spec_lifecycle.reject(
        requirement_id=requirement_id,
        approver=body.approver,
        reason=body.reason
    )
    if not success:
        raise HTTPException(status_code=400, detail="Cannot reject")
    return {"status": "success", "new_status": SpecStatus.DRAFT.value}

class ArchiveBody(BaseModel):
    operator: str
    reason: str = ""

@app.post("/spec/{requirement_id}/archive")
async def archive_spec(requirement_id: str, body: ArchiveBody):
    """归档 OpenSpec"""
    success = spec_lifecycle.archive(
        requirement_id=requirement_id,
        operator=body.operator,
        reason=body.reason
    )
    if not success:
        raise HTTPException(status_code=400, detail="Cannot archive")
    return {"status": "success", "new_status": SpecStatus.ARCHIVED.value}

@app.get("/spec/{requirement_id}/history")
async def get_spec_history(requirement_id: str):
    """获取 OpenSpec 状态变更历史"""
    history = spec_lifecycle.get_history(requirement_id)
    return {"history": [h.dict() for h in history]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
