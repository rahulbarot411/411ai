import subprocess
from app.tools.base import ToolResult

ALLOW = ('ls', 'cat', 'echo', 'pwd', 'python', 'node', 'npm', 'pip')

class BashTool:
    def run(self, cmd: str) -> ToolResult:
        if not cmd.strip().startswith(ALLOW):
            return ToolResult(ok=False, output='command blocked')
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        out = (p.stdout + '\n' + p.stderr)[-8000:]
        return ToolResult(ok=p.returncode == 0, output=out)
