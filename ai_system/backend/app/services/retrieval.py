import json, math, re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from app.core.config import KB_PATH

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")

@dataclass
class Chunk:
    id: str
    topic: str
    text: str

class RetrievalEngine:
    def __init__(self, kb_path: Path = KB_PATH):
        self.kb_path = kb_path
        self.chunks: list[Chunk] = []
        self.df: Counter = Counter()
        self._loaded = False

    def _tokenize(self, text: str) -> list[str]:
        return [t.lower() for t in TOKEN_RE.findall(text)]

    def load(self) -> None:
        if self._loaded:
            return
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                c = Chunk(id=obj['id'], topic=obj['topic'], text=obj['text'])
                self.chunks.append(c)
                self.df.update(set(self._tokenize(c.text)))
        self._loaded = True

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        self.load()
        q = self._tokenize(query)
        qf = Counter(q)
        n = max(1, len(self.chunks))
        scored = []
        for c in self.chunks:
            tokens = self._tokenize(c.text)
            tf = Counter(tokens)
            score = 0.0
            for term, freq in qf.items():
                idf = math.log((n + 1) / (1 + self.df.get(term, 0))) + 1
                score += (tf.get(term, 0) / (len(tokens) + 1)) * idf * freq
            if score > 0:
                scored.append({"id": c.id, "topic": c.topic, "text": c.text, "score": round(score, 5)})
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:top_k]
