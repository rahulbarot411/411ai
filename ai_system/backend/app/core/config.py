from pathlib import Path

BASE_DIR = Path('/app')
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'memory.db'
CACHE_DIR = DATA_DIR / 'cache'
KB_PATH = DATA_DIR / 'index' / 'knowledge.jsonl'
MODEL_BIN = '/usr/local/bin/llama-cli'
MODEL_FILE = str(DATA_DIR / 'models' / 'tinyllama.gguf')
MAX_CONTEXT_CHARS = 12000
