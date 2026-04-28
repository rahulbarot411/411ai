from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel
import aiosqlite
from app.core.config import DB_PATH
from app.services.orchestrator import as_sse

router = APIRouter()

class ChatReq(BaseModel):
    session_id: str | None = None
    message: str

@router.get('/health')
async def health():
    return {'ok': True}

@router.post('/chat')
async def chat(req: ChatReq):
    sid = req.session_id or str(uuid4())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT INTO conversations(session_id,role,content) VALUES(?,?,?)', (sid, 'user', req.message))
        await db.commit()
    resp = as_sse(sid, req.message)
    resp.headers['x-session-id'] = sid
    return resp
