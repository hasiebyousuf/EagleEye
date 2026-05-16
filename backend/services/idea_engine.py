import uuid


async def run_pipeline(
    report_id: uuid.UUID,
    mode: str,
    idea: str | None,
    budget: float,
    market_focus: str | None,
    workspace_id: uuid.UUID,
) -> None:
    raise NotImplementedError("IdeaEngine pipeline not yet implemented — Task 12")
