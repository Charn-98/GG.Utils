from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

@dataclass(frozen=True)
class LowestPriceResult(BaseModel):
    """Output model for API response for a single item"""
    article_number: str
    lowest_price: Decimal
    is_promo: bool
    valid_from: date
    valid_to: date