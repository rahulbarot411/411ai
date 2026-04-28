from pydantic import BaseModel

class ToolResult(BaseModel):
    ok: bool
    output: str
