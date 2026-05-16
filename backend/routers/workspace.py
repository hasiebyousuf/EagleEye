from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from core.supabase import get_supabase
from core.config import settings
from models.workspace import WorkspaceCreate, WorkspaceResponse
import httpx

router = APIRouter(prefix="/workspace", tags=["workspace"])


async def get_user_id_from_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.removeprefix("Bearer ")
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.supabase_anon_key,
            },
        )
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return res.json()["id"]


@router.post("", status_code=201, response_model=WorkspaceResponse)
async def create_workspace(
    body: WorkspaceCreate,
    authorization: Optional[str] = Header(default=None),
):
    owner_id = await get_user_id_from_token(authorization)
    supabase = get_supabase()

    existing = supabase.table("workspaces").select("id").eq("owner_id", owner_id).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Workspace already exists")

    result = supabase.table("workspaces").insert({
        "owner_id": owner_id,
        "name": body.name,
        "budget": body.budget,
        "currency": body.currency,
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create workspace")

    return result.data[0]


@router.get("", response_model=WorkspaceResponse)
async def get_workspace(authorization: Optional[str] = Header(default=None)):
    owner_id = await get_user_id_from_token(authorization)
    supabase = get_supabase()

    result = supabase.table("workspaces").select("*").eq("owner_id", owner_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="No workspace found")

    return result.data[0]
