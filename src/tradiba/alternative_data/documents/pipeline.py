from typing import Any

class DocumentPipeline:
    """
    Extracts structures, entities, and relationships from PDFs and reports.
    """
    def extract_entities(self, document: Any) -> list:
        return ["EntityA", "EntityB"]
