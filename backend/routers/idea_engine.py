from fastapi import APIRouter, HTTPException
import uuid

router = APIRouter(prefix="/idea-engine", tags=["idea-engine"])


@router.post("/run")
async def run_idea_engine():
    raise HTTPException(status_code=501, detail="Not implemented — Task 13")


@router.get("/report/{report_id}")
async def get_report(report_id: uuid.UUID):
    raise HTTPException(status_code=501, detail="Not implemented — Task 13")
