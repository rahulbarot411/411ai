# AI System (single container)

## Run
```bash
docker build -t ai-system -f ai_system/Dockerfile .
docker run -d -p 8080:8080 ai-system
```

Open `http://localhost:8080`.

## CLI
Inside container:
```bash
ai-cli "how to set kubernetes memory limits"
```

## Architecture
- FastAPI backend with SSE streaming
- Retrieval-first pipeline (BM25-like lexical scorer)
- Template-guided small-model generation layer
- SQLite memory, cache, and chat archive
- Tool subsystem (file read/write, bash, http fetch)
- React-style web UI

## Optimizations for t2.medium
- Lazy model load (first request only)
- Retrieval index preloaded from JSONL
- SQLite cache for repeated prompts
- Context compression by truncating historic turns
- Streaming response tokens to reduce perceived latency
