from httpx import AsyncClient


async def get_client():
    client = AsyncClient(timeout=10)
    try:
        yield client
    finally:
        await client.aclose()
