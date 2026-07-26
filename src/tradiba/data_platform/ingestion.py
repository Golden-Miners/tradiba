from typing import Any
from tradiba.data_platform.validation import DataQualityValidator
from tradiba.data_platform.lakehouse import DataLakehouse, StorageZone
from uuid import UUID

class IngestionPipeline:
    """ETL pipeline for dataset ingestion into the Data Lakehouse."""
    def __init__(self, lakehouse: DataLakehouse, validator: DataQualityValidator) -> None:
        self.lakehouse = lakehouse
        self.validator = validator

    def run(self, dataset_id: UUID, raw_data: list[dict[str, Any]], expected_schema: set[str]) -> bool:
        """Executes the standard ingestion workflow (Raw -> Validate -> Curated)."""
        # Load to Raw
        self.lakehouse.write_to_zone(StorageZone.RAW, dataset_id, raw_data)
        
        # Validate
        self.validator.validate_schema(raw_data, expected_schema)
        
        # Load to Curated (assuming simple pass-through for now)
        self.lakehouse.write_to_zone(StorageZone.CURATED, dataset_id, raw_data)
        
        return True
