from dataclasses import dataclass, field
import os

@dataclass
class ResearchConfig:
    artifact_storage_path: str = field(default_factory=lambda: os.getenv("ARTIFACT_STORAGE_PATH", "/tmp/tradiba/models"))
    default_validation_split: float = 0.2
