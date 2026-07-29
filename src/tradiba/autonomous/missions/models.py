from dataclasses import dataclass

@dataclass
class Mission:
    id: str
    goal: str
    status: str
    autonomy_level: int
