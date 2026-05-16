from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings  # noqa: F401 — fails fast if env vars missing
from routers import workspace, idea_engine

app = FastAPI(title="EagleEye API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspace.router)
app.include_router(idea_engine.router)


@app.get("/health")
def health():
    return {"status": "ok"}
