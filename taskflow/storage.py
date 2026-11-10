import json
from dataclasses import asdict
from pathlib import Path

from .models import Task


class JsonStorage:
    def __init__(self, path="tasks.json"):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return []
        with open(self.path) as f:
            return [Task(**item) for item in json.load(f)]

    def save(self, tasks):
        with open(self.path, "w") as f:
            json.dump([asdict(t) for t in tasks], f, indent=2)
