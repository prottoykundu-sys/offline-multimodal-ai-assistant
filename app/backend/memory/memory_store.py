import json
from pathlib import Path

class MemoryStore:
    def __init__(self, path="memory.json"):
        self.path = Path(path)

    def save(self, data):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    def read_all(self):
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        return lines
