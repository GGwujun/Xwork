from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Requirement(BaseModel):
    summary: str = Field(..., description="High level summary of the requirement")
    description: str = Field(..., description="Detailed description")
    acceptance_criteria: List[str] = Field(default_factory=list, description="List of criteria to verify the requirement")

class ApiEndpoint(BaseModel):
    method: str
    path: str
    description: str
    request_model: Optional[Dict[str, Any] | str] = None
    response_model: Optional[Dict[str, Any] | str] = None

class DataModel(BaseModel):
    name: str
    fields: List[Dict[str, str | bool]]

class Design(BaseModel):
    architecture_overview: str
    api_endpoints: List[ApiEndpoint] = Field(default_factory=list)
    data_models: List[DataModel] = Field(default_factory=list)
    tech_stack: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)


class WorkflowNode(BaseModel):
    id: str
    type: str
    label: str
    data: Dict[str, Any] = Field(default_factory=dict)


class WorkflowEdge(BaseModel):
    source: str
    target: str
    type: str = "default"


class Workflow(BaseModel):
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)


class Collaboration(BaseModel):
    owner: str
    collaborators: List[str] = Field(default_factory=list)
    shared: bool = True


class Metadata(BaseModel):
    created_at: str
    updated_at: str
    tfs_work_item_id: Optional[str] = None

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed|failed)$")
    file_changes: List[str] = Field(default_factory=list, description="List of files to be modified/created")
    assigned_agent: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)

class OpenSpec(BaseModel):
    spec_version: str = "0.2.0"
    project_name: str
    requirement: Requirement
    design: Optional[Design] = None
    tasks: List[Task] = Field(default_factory=list)
    workflow: Optional[Workflow] = None
    collaboration: Optional[Collaboration] = None
    metadata: Optional[Metadata] = None
