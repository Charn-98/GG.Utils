from abc import ABC, abstractmethod
from typing import List
from src.models.selling_record import SellingRecord
from src.models.promotion_record import PromotionRecord


class IPriceRepository(ABC):
    """Interface defining the contract for data access.
    The service layer will only interact with this interface which inforces
    decoupling
    """

    @abstractmethod
    def get_all_selling_prices(self) -> List[SellingRecord]:
        """Fetches all regular selling prices with pagination"""
        pass

    @abstractmethod
    def get_all_promotion_prices(self) -> List[PromotionRecord]:
        """Fetches all promptional selling prices with pagination"""
        pass

    @abstractmethod
    def get_selling_price_by_article(self, article_number: str) -> List[SellingRecord]:
        """Fetches a single regular selling price"""
        pass

    @abstractmethod
    def get_promotion_price_by_article(self, article_number: str) -> List[PromotionRecord]:
        """Fetches a single promptional selling price"""
        pass