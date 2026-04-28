import asyncio
from app.services.templates import select_template

class LocalModel:
    def __init__(self):
        self.loaded = False

    async def ensure_loaded(self):
        if not self.loaded:
            await asyncio.sleep(0.05)
            self.loaded = True

    async def stream_generate(self, prompt: str):
        await self.ensure_loaded()
        # Placeholder streaming logic; replace with llama.cpp subprocess stream in production
        response = f"{select_template(prompt)}\n\nSynthesized response:\n{prompt[:1200]}"
        for i in range(0, len(response), 28):
            await asyncio.sleep(0.01)
            yield response[i:i+28]
