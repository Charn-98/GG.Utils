from src.models.base_record import BaseRecord
from datetime import date
from decimal import Decimal

class PromotionRecord(BaseRecord):
    """Record for the promotional price"""
    compaign_period: int
    promotion_number: int
    promotion_description: str
    promotion_start_date: date
    promotion_end_date: date
    status: str
    original_price: Decimal
    sale_price: Decimal