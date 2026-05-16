class DataFetchError(Exception):
    pass


async def fetch_serp_data(keyword: str, region: str = "us") -> dict:
    raise NotImplementedError("SerpAPI service not yet implemented — Task 10")
