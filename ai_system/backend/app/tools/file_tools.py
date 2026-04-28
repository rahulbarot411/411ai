from pathlib import Path
from app.tools.base import ToolResult

SAFE_ROOT = Path('/workspace')

class FileReadTool:
    def run(self, path: str) -> ToolResult:
        p = Path(path).resolve()
        if SAFE_ROOT not in p.parents and p != SAFE_ROOT:
            return ToolResult(ok=False, output='permission denied')
        return ToolResult(ok=True, output=p.read_text(encoding='utf-8')[:20000])

class FileWriteTool:
    def run(self, path: str, content: str) -> ToolResult:
        p = Path(path).resolve()
        if SAFE_ROOT not in p.parents and p != SAFE_ROOT:
            return ToolResult(ok=False, output='permission denied')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return ToolResult(ok=True, output='written')
