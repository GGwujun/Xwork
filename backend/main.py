from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.schemas import OpenSpec, Requirement
from app.agent_swarm import agent_swarm
from app.tfs_mcp import mcp_list_work_items, mcp_get_work_item, mcp_create_work_item, mcp_trigger_build
from app.checkin_guard import validate_before_checkin
from app.session_sync import save_current_session, get_share_link, session_sync
import uuid

app = FastAPI(title="Enterprise Forge Engine")

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

# --- Spec Generation ---

@app.post("/spec/generate", response_model=OpenSpec)
async def generate_spec(requirement: Requirement):
    """Generate OpenSpec using Agent Swarm (PM + Architect)."""
    spec = await agent_swarm.generate_spec(requirement)
    return spec

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


