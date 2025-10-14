from dataclasses import dataclass
from src.models.base import BaseRecord
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class SellingRecord(BaseRecord):
    """Record for the selling price"""
    price_effective_date: date
    price_expiry_date: date
    price: Decimal