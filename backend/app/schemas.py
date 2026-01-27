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
    request_model: Optional[Dict[str, Any]] = None
    response_model: Optional[Dict[str, Any]] = None

class DataModel(BaseModel):
    name: str
    fields: Dict[str, str]

class Design(BaseModel):
    architecture_overview: str
    api_endpoints: List[ApiEndpoint] = Field(default_factory=list)
    data_models: List[DataModel] = Field(default_factory=list)

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed|failed)$")
    file_changes: List[str] = Field(default_factory=list, description="List of files to be modified/created")

class OpenSpec(BaseModel):
    spec_version: str = "0.1.0"
    project_name: str
    requirement: Requirement
    design: Optional[Design] = None
    tasks: List[Task] = Field(default_factory=list)
