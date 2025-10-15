from src.services.price_service import PriceService
from src.repositories.interface import IPriceRepository

def get_price_service() -> PriceService:
    """
    Dependency Injection contract for the PriceService.
    This function is overridden in main.py to return the singleton instance.
    """
    pass
