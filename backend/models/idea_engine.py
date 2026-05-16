from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class IdeaEngineRunRequest(BaseModel):
    mode: str  # 'validate' | 'generate'
    input_idea: Optional[str] = None
    budget: float
    market_focus: Optional[str] = None


class IdeaEngineRunResponse(BaseModel):
    report_id: uuid.UUID


class ReportSectionResponse(BaseModel):
    id: uuid.UUID
    report_id: uuid.UUID
    section_type: str
    content: dict
    created_at: datetime


class IdeaReportResponse(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    mode: str
    input_idea: Optional[str]
    budget: float
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    sections: list[ReportSectionResponse] = []
