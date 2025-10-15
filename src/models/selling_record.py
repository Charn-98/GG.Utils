from dataclasses import dataclass
from models.base_record import BaseRecord
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class SellingRecord(BaseRecord):
    """Record for the selling price"""
    price_start_date: date
    price_end_date: date
    price: Decimal