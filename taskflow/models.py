from dataclasses import dataclass

PRIORITIES = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    due: str | None = None  # fecha ISO: YYYY-MM-DD
