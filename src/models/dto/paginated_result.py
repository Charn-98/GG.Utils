from dataclasses import dataclass
from typing import List, TypeVar, Generic

#define the generic T that can be any type
T = TypeVar('T')

@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    """General model for paginated data"""
    data: List[T]
    total_count: int
    page_number: int
    page_size: int