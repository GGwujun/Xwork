"""
TFS MCP Server - Model Context Protocol adapter for Azure DevOps / TFS.

This module provides standard MCP tools for interacting with TFS/Azure DevOps:
- list_work_items: List work items from a project
- get_work_item: Get details of a specific work item
- create_work_item: Create a new bug/task/user story
- trigger_build: Trigger a CI build pipeline
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os

# --- Types ---

class WorkItem(BaseModel):
    id: int
    title: str
    type: str  # Bug, Task, UserStory, Feature
    state: str
    assigned_to: Optional[str] = None
    description: Optional[str] = None

class CreateWorkItemRequest(BaseModel):
    project: str
    type: str
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None

# --- TFS Client (Stub) ---

class TfsClient:
    """
    Client for Azure DevOps / TFS REST API.
    In production, this uses the azure-devops Python SDK or direct REST calls.
    """
    
    def __init__(self):
        self.base_url = os.environ.get("TFS_URL", "https://dev.azure.com/winning")
        self.pat = os.environ.get("TFS_PAT", "")  # Personal Access Token
        self._mock_items: List[WorkItem] = [
            WorkItem(id=1001, title="Setup Authentication", type="UserStory", state="Active"),
            WorkItem(id=1002, title="Fix login bug", type="Bug", state="New"),
            WorkItem(id=1003, title="Implement patient CRUD", type="Task", state="Active", assigned_to="dev@winning.com"),
        ]
    
    def is_connected(self) -> bool:
        """Check if we have valid credentials."""
        return bool(self.pat)

    async def list_work_items(self, project: str, item_type: Optional[str] = None) -> List[WorkItem]:
        """List work items, optionally filtered by type."""
        # In production: Use WIQL query via REST API
        items = self._mock_items
        if item_type:
            items = [i for i in items if i.type.lower() == item_type.lower()]
        return items

    async def get_work_item(self, item_id: int) -> Optional[WorkItem]:
        """Get a specific work item by ID."""
        for item in self._mock_items:
            if item.id == item_id:
                return item
        return None

    async def create_work_item(self, request: CreateWorkItemRequest) -> WorkItem:
        """Create a new work item."""
        new_id = max(i.id for i in self._mock_items) + 1 if self._mock_items else 1
        new_item = WorkItem(
            id=new_id,
            title=request.title,
            type=request.type,
            state="New",
            assigned_to=request.assigned_to,
            description=request.description,
        )
        self._mock_items.append(new_item)
        return new_item

    async def trigger_build(self, project: str, pipeline_id: int) -> Dict[str, Any]:
        """Trigger a build pipeline."""
        # In production: POST to /_apis/build/builds
        return {
            "build_id": 12345,
            "status": "queued",
            "pipeline_id": pipeline_id,
            "project": project,
        }

# --- MCP Tool Definitions ---

tfs_client = TfsClient()

async def mcp_list_work_items(project: str, item_type: Optional[str] = None) -> List[Dict]:
    """MCP Tool: List work items from TFS."""
    items = await tfs_client.list_work_items(project, item_type)
    return [item.model_dump() for item in items]

async def mcp_get_work_item(item_id: int) -> Optional[Dict]:
    """MCP Tool: Get a work item by ID."""
    item = await tfs_client.get_work_item(item_id)
    return item.model_dump() if item else None

async def mcp_create_work_item(project: str, item_type: str, title: str, description: str = "", assigned_to: str = "") -> Dict:
    """MCP Tool: Create a new work item."""
    request = CreateWorkItemRequest(
        project=project,
        type=item_type,
        title=title,
        description=description or None,
        assigned_to=assigned_to or None,
    )
    item = await tfs_client.create_work_item(request)
    return item.model_dump()

async def mcp_trigger_build(project: str, pipeline_id: int) -> Dict:
    """MCP Tool: Trigger a CI/CD pipeline."""
    return await tfs_client.trigger_build(project, pipeline_id)
