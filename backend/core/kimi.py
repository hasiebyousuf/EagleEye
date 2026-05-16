from core.config import settings


class KimiClient:
    def __init__(self):
        self.api_key = settings.kimi_api_key
        self.base_url = "https://api.moonshot.cn/v1"

    async def complete(self, system_prompt: str, user_message: str) -> dict:
        raise NotImplementedError("Kimi client not yet implemented — Task 11")
