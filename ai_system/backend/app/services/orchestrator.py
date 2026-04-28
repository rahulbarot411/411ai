import hashlib
import json
from fastapi.responses import StreamingResponse
import aiosqlite
from app.core.config import DB_PATH
from app.services.retrieval import RetrievalEngine
from app.services.model import LocalModel
from app.services.compression import compress_history

retrieval = RetrievalEngine()
model = LocalModel()

async def _get_messages(session_id: str) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute('SELECT role, content FROM conversations WHERE session_id=? ORDER BY id', (session_id,))
        rows = await cur.fetchall()
    return [{"role":r[0], "content":r[1]} for r in rows]

async def _cache_get(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute('SELECT value FROM cache WHERE key=?', (key,))
        row = await cur.fetchone()
    return row[0] if row else None

async def _cache_set(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT OR REPLACE INTO cache(key,value) VALUES(?,?)', (key, value))
        await db.commit()

async def stream_reply(session_id: str, user_text: str):
    msgs = await _get_messages(session_id)
    context = compress_history(msgs)
    chunks = retrieval.search(user_text)
    retrieval_text = "\n".join([f"[{c['topic']}] {c['text']}" for c in chunks])
    prompt = f"Context:\n{context}\n\nRetrieved:\n{retrieval_text}\n\nUser:{user_text}"
    key = hashlib.sha256(prompt.encode()).hexdigest()
    cached = await _cache_get(key)
    if cached:
        yield f"data: {json.dumps({'delta': cached, 'done': True})}\n\n"
        return

    acc = ""
    async for tok in model.stream_generate(prompt):
        acc += tok
        yield f"data: {json.dumps({'delta': tok, 'done': False})}\n\n"
    await _cache_set(key, acc)
    yield f"data: {json.dumps({'delta': '', 'done': True})}\n\n"

def as_sse(session_id: str, user_text: str):
    return StreamingResponse(stream_reply(session_id, user_text), media_type='text/event-stream')
