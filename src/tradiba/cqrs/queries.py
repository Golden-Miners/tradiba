"""
CQRS Queries.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Query:
    """Base class for all queries."""
    pass
