import httpx
from app.tools.base import ToolResult

class HTTPFetchTool:
    async def run(self, url: str) -> ToolResult:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            return ToolResult(ok=r.is_success, output=r.text[:12000])
