class ResearchError(Exception):
    """Base exception for quantitative research operations."""
    pass

class ModelNotFittedError(ResearchError):
    pass

class PipelineError(ResearchError):
    pass

class ValidationError(ResearchError):
    pass
