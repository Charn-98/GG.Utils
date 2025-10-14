from dataclasses import dataclass
from src.models.base import BaseRecord
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class LowestPriceResult():
    """Output model for API response for a single item"""
    article_number: str
    lowest_price: Decimal
    is_promo: bool
    valid_from: date
    valid_to: date