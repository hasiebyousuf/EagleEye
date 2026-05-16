from pydantic import BaseModel
import uuid
from datetime import datetime


class WorkspaceCreate(BaseModel):
    name: str
    budget: float
    currency: str = "USD"


class WorkspaceResponse(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    budget: float
    currency: str
    created_at: datetime
