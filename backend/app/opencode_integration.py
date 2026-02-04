"""
OpenCode集成服务模块
用于直接调用OpenCode引擎生成OpenSpec规范
"""

import json
import uuid
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import httpx
from pydantic import ValidationError

from .schemas import OpenSpec, Requirement, Design, Task, ApiEndpoint, DataModel, Metadata
from .prompts.templates import build_opencode_spec_prompt

logger = logging.getLogger(__name__)


class OpenCodeError(Exception):
    """OpenCode集成相关错误"""
    pass


class OpenCodeSpecGenerator:
    """OpenCode规范生成器"""

    def __init__(self, opencode_url: str = None):
        # 支持多种方式获取OpenCode服务URL
        # 优先级：参数 > OpenWork桥接 > 环境变量 > 默认值
        import os
        if opencode_url is None:
            # 尝试从OpenWork获取
            try:
                from .openwork_bridge import get_openwork_bridge
                bridge = get_openwork_bridge()
                opencode_url = bridge.get_opencode_url()
                if opencode_url:
                    logger.info(f"从OpenWork获取到OpenCode服务URL: {opencode_url}")
            except Exception as e:
                logger.debug(f"无法从OpenWork获取URL: {str(e)}")

            # 如果OpenWork没有提供，使用环境变量或默认值
            if not opencode_url:
                opencode_url = os.getenv('OPENCODE_URL', 'http://127.0.0.1:4096')
                logger.info(f"使用配置的OpenCode服务URL: {opencode_url}")

        self.opencode_url = opencode_url.rstrip('/')
        self.timeout = 300  # 5分钟超时
        self.session_timeout = 60  # session创建超时

    async def generate_spec(
        self,
        requirement: Requirement,
        workspace_path: Optional[str] = None
    ) -> OpenSpec:
        """
        使用OpenCode生成OpenSpec规范

        Args:
            requirement: 需求信息
            workspace_path: 工作区路径（可选）

        Returns:
            OpenSpec: 生成的规范

        Raises:
            OpenCodeError: 生成过程中的错误
        """
        session_id = None
        try:
            logger.info(f"开始使用OpenCode生成规范: {requirement.summary}")

            # 1. 创建临时session
            session_id = await self._create_temporary_session(workspace_path)
            logger.info(f"创建临时session: {session_id}")

            # 2. 构建上下文信息
            context = await self._build_context(workspace_path)

            # 3. 发送生成prompt
            response = await self._send_spec_generation_prompt(
                session_id, requirement, context
            )
            logger.info("收到OpenCode响应，开始解析")

            # 4. 解析响应并转换为OpenSpec格式
            spec = await self._parse_opencode_response(response, requirement)
            logger.info(f"成功生成OpenSpec: {spec.project_name}")

            return spec

        except Exception as e:
            logger.error(f"OpenCode生成规范失败: {str(e)}")
            raise OpenCodeError(f"生成规范失败: {str(e)}") from e

        finally:
            # 5. 清理临时session
            if session_id:
                try:
                    await self._cleanup_session(session_id)
                    logger.info(f"清理临时session: {session_id}")
                except Exception as e:
                    logger.warning(f"清理session失败: {str(e)}")

    async def _create_temporary_session(self, workspace_path: Optional[str] = None) -> str:
        """创建临时session"""
        try:
            async with httpx.AsyncClient(timeout=self.session_timeout) as client:
                payload = {
                    "title": f"OpenSpec生成-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                }
                if workspace_path:
                    payload["directory"] = workspace_path

                response = await client.post(
                    f"{self.opencode_url}/api/session/create",
                    json=payload
                )
                response.raise_for_status()

                # 检查响应内容
                response_text = response.text
                logger.info(f"OpenCode API 响应: status={response.status_code}, content_length={len(response_text)}, content={response_text[:200]}")

                if not response_text:
                    raise OpenCodeError("创建session失败：API返回空响应")

                try:
                    result = response.json()
                except Exception as e:
                    logger.error(f"解析JSON失败: {e}, 原始响应: {response_text}")
                    raise OpenCodeError(f"创建session失败：无法解析响应 - {response_text[:100]}")

                if result.get("data") and result["data"].get("id"):
                    return result["data"]["id"]
                else:
                    raise OpenCodeError(f"创建session失败：响应格式不正确 - {result}")

        except httpx.TimeoutException:
            raise OpenCodeError("创建session超时")
        except httpx.HTTPStatusError as e:
            raise OpenCodeError(f"创建session失败：HTTP {e.response.status_code}")
        except Exception as e:
            raise OpenCodeError(f"创建session失败：{str(e)}")

    async def _build_context(self, workspace_path: Optional[str] = None) -> str:
        """构建上下文信息"""
        context_parts = []

        # 基础上下文
        context_parts.append("## 项目上下文")
        context_parts.append("这是一个基于OpenWork的项目，需要生成符合OpenSpec v0.2.0规范的技术文档。")

        if workspace_path:
            context_parts.append(f"工作区路径: {workspace_path}")

        # 技术栈信息
        context_parts.append("\n## 技术栈")
        context_parts.append("- 前端: SolidJS + TailwindCSS")
        context_parts.append("- 后端: FastAPI + Python")
        context_parts.append("- 数据库: PostgreSQL/Redis")
        context_parts.append("- 部署: Docker + Kubernetes")

        return "\n".join(context_parts)

    async def _send_spec_generation_prompt(
        self,
        session_id: str,
        requirement: Requirement,
        context: str
    ) -> str:
        """发送生成prompt并获取响应"""
        try:
            # 构建prompt
            prompt = build_opencode_spec_prompt(requirement, context)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 发送prompt
                response = await client.post(
                    f"{self.opencode_url}/api/session/prompt",
                    json={
                        "sessionID": session_id,
                        "model": "claude-3-5-sonnet-20241022",  # 使用高质量模型
                        "parts": [{"type": "text", "text": prompt}]
                    }
                )
                response.raise_for_status()

                # 等待响应完成
                await asyncio.sleep(2)  # 给一点时间让响应开始

                # 获取session消息
                messages_response = await client.get(
                    f"{self.opencode_url}/api/session/messages",
                    params={"sessionID": session_id}
                )
                messages_response.raise_for_status()

                messages_data = messages_response.json()
                if not messages_data.get("data"):
                    raise OpenCodeError("获取消息失败：无数据")

                # 找到最后一条助手消息
                messages = messages_data["data"]
                for message in reversed(messages):
                    if message.get("role") == "assistant":
                        # 获取消息内容
                        parts_response = await client.get(
                            f"{self.opencode_url}/api/session/message/{message['id']}/parts"
                        )
                        parts_response.raise_for_status()

                        parts_data = parts_response.json()
                        if parts_data.get("data"):
                            # 合并所有文本部分
                            content_parts = []
                            for part in parts_data["data"]:
                                if part.get("type") == "text" and part.get("text"):
                                    content_parts.append(part["text"])

                            if content_parts:
                                return "".join(content_parts)

                raise OpenCodeError("未找到有效的助手响应")

        except httpx.TimeoutException:
            raise OpenCodeError("生成规范超时")
        except httpx.HTTPStatusError as e:
            raise OpenCodeError(f"生成规范失败：HTTP {e.response.status_code}")
        except Exception as e:
            raise OpenCodeError(f"生成规范失败：{str(e)}")

    async def _parse_opencode_response(
        self,
        response: str,
        requirement: Requirement
    ) -> OpenSpec:
        """解析OpenCode响应并转换为OpenSpec格式"""
        try:
            # 尝试从响应中提取JSON
            json_content = self._extract_json_from_response(response)

            if not json_content:
                # 如果没有找到JSON，尝试解析Markdown格式的响应
                return self._parse_markdown_response(response, requirement)

            # 验证和转换JSON数据
            return self._convert_json_to_openspec(json_content, requirement)

        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            # 降级处理：创建基础的OpenSpec
            return self._create_fallback_spec(requirement, response)

    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """从响应中提取JSON内容"""
        try:
            # 查找JSON代码块
            import re
            json_pattern = r'```json\s*\n(.*?)\n```'
            matches = re.findall(json_pattern, response, re.DOTALL)

            if matches:
                json_str = matches[0].strip()
                return json.loads(json_str)

            # 尝试直接解析整个响应
            response_clean = response.strip()
            if response_clean.startswith('{') and response_clean.endswith('}'):
                return json.loads(response_clean)

            return None

        except json.JSONDecodeError:
            return None

    def _convert_json_to_openspec(
        self,
        json_data: Dict[str, Any],
        requirement: Requirement
    ) -> OpenSpec:
        """将JSON数据转换为OpenSpec格式"""
        try:
            # 基础字段
            spec_data = {
                "spec_version": json_data.get("spec_version", "0.2.0"),
                "project_name": json_data.get("project_name", f"Project-{uuid.uuid4().hex[:8]}"),
                "requirement": requirement.dict()
            }

            # 设计信息
            if "design" in json_data:
                design_data = json_data["design"]
                design = Design(
                    architecture_overview=design_data.get("architecture_overview", ""),
                    api_endpoints=[
                        ApiEndpoint(**ep) for ep in design_data.get("api_endpoints", [])
                    ],
                    data_models=[
                        DataModel(**dm) for dm in design_data.get("data_models", [])
                    ],
                    tech_stack=design_data.get("tech_stack", {}),
                    dependencies=design_data.get("dependencies", [])
                )
                spec_data["design"] = design

            # 任务列表
            if "tasks" in json_data:
                tasks = []
                for task_data in json_data["tasks"]:
                    task = Task(
                        id=task_data.get("id", str(uuid.uuid4())),
                        title=task_data.get("title", ""),
                        description=task_data.get("description", ""),
                        status=task_data.get("status", "pending"),
                        file_changes=task_data.get("file_changes", []),
                        assigned_agent=task_data.get("assigned_agent"),
                        dependencies=task_data.get("dependencies", [])
                    )
                    tasks.append(task)
                spec_data["tasks"] = tasks

            # 元数据
            now = datetime.now().isoformat()
            spec_data["metadata"] = Metadata(
                created_at=now,
                updated_at=now
            )

            return OpenSpec(**spec_data)

        except ValidationError as e:
            logger.error(f"数据验证失败: {str(e)}")
            raise OpenCodeError(f"生成的数据格式不正确: {str(e)}")

    def _parse_markdown_response(
        self,
        response: str,
        requirement: Requirement
    ) -> OpenSpec:
        """解析Markdown格式的响应"""
        # 简单的Markdown解析逻辑
        lines = response.split('\n')

        # 提取项目名称
        project_name = f"Project-{uuid.uuid4().hex[:8]}"
        for line in lines:
            if line.startswith('# ') and 'project' in line.lower():
                project_name = line[2:].strip()
                break

        # 提取架构概述
        architecture_overview = ""
        in_architecture = False
        for line in lines:
            if '架构' in line or 'architecture' in line.lower():
                in_architecture = True
                architecture_overview = line + '\n'
            elif in_architecture and line.strip():
                architecture_overview += line + '\n'
            elif in_architecture and not line.strip():
                break

        # 创建基础任务
        tasks = [
            Task(
                id=str(uuid.uuid4()),
                title="实现核心功能",
                description="根据需求实现核心功能",
                status="pending",
                file_changes=[]
            )
        ]

        now = datetime.now().isoformat()

        return OpenSpec(
            project_name=project_name,
            requirement=requirement,
            design=Design(architecture_overview=architecture_overview),
            tasks=tasks,
            metadata=Metadata(created_at=now, updated_at=now)
        )

    def _create_fallback_spec(
        self,
        requirement: Requirement,
        response: str
    ) -> OpenSpec:
        """创建降级的OpenSpec"""
        now = datetime.now().isoformat()

        return OpenSpec(
            project_name=f"Project-{uuid.uuid4().hex[:8]}",
            requirement=requirement,
            design=Design(
                architecture_overview=f"# 技术架构\n\n基于需求生成的架构说明：\n\n{response[:500]}..."
            ),
            tasks=[
                Task(
                    id=str(uuid.uuid4()),
                    title="分析需求",
                    description=requirement.description,
                    status="pending",
                    file_changes=[]
                ),
                Task(
                    id=str(uuid.uuid4()),
                    title="设计架构",
                    description="设计系统架构和技术方案",
                    status="pending",
                    file_changes=[]
                ),
                Task(
                    id=str(uuid.uuid4()),
                    title="实现功能",
                    description="实现核心功能",
                    status="pending",
                    file_changes=[]
                )
            ],
            metadata=Metadata(created_at=now, updated_at=now)
        )

    async def _cleanup_session(self, session_id: str):
        """清理临时session"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # 尝试删除session（如果OpenCode支持的话）
                # 这里可能需要根据实际的OpenCode API调整
                response = await client.delete(
                    f"{self.opencode_url}/api/session/{session_id}"
                )
                # 不强制要求成功，因为有些OpenCode版本可能不支持删除

        except Exception as e:
            # 清理失败不影响主流程
            logger.warning(f"清理session {session_id} 失败: {str(e)}")


# 全局实例
_generator_instance = None


def get_opencode_generator(opencode_url: str = None) -> OpenCodeSpecGenerator:
    """获取OpenCode生成器实例"""
    global _generator_instance
    if _generator_instance is None or _generator_instance.opencode_url != opencode_url:
        _generator_instance = OpenCodeSpecGenerator(opencode_url)
    return _generator_instance