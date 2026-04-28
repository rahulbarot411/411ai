from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.core.db import init_db

app = FastAPI(title="ai-system")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.mount("/", StaticFiles(directory="/app/frontend", html=True), name="frontend")


@app.on_event("startup")
async def startup() -> None:
    await init_db()
