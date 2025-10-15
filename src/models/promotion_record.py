from dataclasses import dataclass
from models.base_record import BaseRecord
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class PromotionRecord(BaseRecord):
    """Record for the promotional price"""
    compaign_period: date
    promotion_number: int
    promotion_description: str
    promption_start_date: date
    promption_end_date: date
    status: str
    original_price: Decimal
    sale_price: Decimal