from dataclasses import dataclass

@dataclass
class StorageConfig:
    """Configuration for data lakehouse storage zones."""
    raw_path: str = "/data/raw"
    validated_path: str = "/data/validated"
    curated_path: str = "/data/curated"
    archive_path: str = "/data/archive"

@dataclass
class RetentionPolicyConfig:
    """Configurable lifecycle rules."""
    tick_data_days: int = 5 * 365
    order_events_days: int = 7 * 365
    audit_logs_days: int = 10 * 365
    metrics_days: int = int(1.5 * 365)
    research_days: int = 90
