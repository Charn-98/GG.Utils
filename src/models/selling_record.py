from src.models.base_record import BaseRecord
from datetime import date
from decimal import Decimal

class SellingRecord(BaseRecord):
    """Record for the selling price"""
    price_start_date: date
    price_end_date: date
    price: Decimal