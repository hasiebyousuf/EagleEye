class DataFetchError(Exception):
    pass


async def fetch_trends(keyword: str, region: str = "US") -> dict:
    raise NotImplementedError("Google Trends service not yet implemented — Task 9")
