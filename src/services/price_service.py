from src.repositories.interface import IPriceRepository
from typing import Optional, List, Set
from src.models.selling_record import SellingRecord
from src.models.promotion_record import PromotionRecord
from datetime import date, timedelta
from src.models.dto.lowest_price_result import LowestPriceResult
from decimal import Decimal
import sys

class PriceService:
    """
    Handles the business logic. In this case,
    To calculate the lowest price for an item
    over the last 30 days
    """
    LAST_X_DAYS = 30

    def __init__(self, repository: IPriceRepository):
        """
        Perform dependency injection to initialize repository.

        Args:
            repository (IPriceRepository): _description_
        """
        self._repository = repository
        self._all_article_numbers: Optional[Set[str]] = None
        self._all_selling_prices: List[SellingRecord] = []
        self._all_promotion_prices: List[PromotionRecord] = []

        self._preload_data()

    def _preload_data(self):
        """
        Loads all data from the repository once for in-memory processing.
        """
        self._all_selling_prices = self._repository.get_all_selling_prices()
        self._all_promotions = self._repository.get_all_promotion_prices()

        selling_article_numbers = {r.article_number for r in self._all_selling_prices}
        promotion_article_numbers = {r.article_number for r in self._all_promotions}
        #union the Article numbers for a unique item/article list
        self._all_article_numbers = selling_article_numbers.union(promotion_article_numbers)

    def get_all_article_numbers(self) -> Set[str]:
        """Returns a set of all unique article/Article numbers found in the data."""
        return self._all_article_numbers or set()

    def calculate_lowest_price_x_days(self, article_number: str, today: date) -> LowestPriceResult:
        """
        Calculates the lowest price for a single item over the last X days.

        Args:
            article_number: The item identifier.
            today: The date to calculate the lookback period from (e.g., date.today()).

        Returns:
            A LowestPriceResult object with the best price found.
        """
        x_days_ago = today - timedelta(days=self.LAST_X_DAYS)

        lowest_price = sys.float_info.max
        best_price_valid_from = today
        best_price_valid_to = today
        is_promo = False

        selling_prices = [
            r for r in self._all_selling_prices if r.article_number == article_number
        ]

        for record in selling_prices:
            is_active_within_window = (
                record.price_start_date <= today and
                record.price_end_date >= x_days_ago
            )

            if is_active_within_window:
                if record.price < lowest_price:
                    lowest_price = record.price
                    best_price_valid_from = record.price_start_date
                    best_price_valid_to = record.price_end_date
                    is_promo = False

        promotions = [
            p for p in self._all_promotions if p.article_number == article_number
        ]

        #if we find a promotion that is less than the selling price, then we update the values
        for record in promotions:
            is_active_within_window = (
                record.promotion_start_date <= today and
                record.promotion_end_date >= x_days_ago
            )

            #assuming 40 is valid
            is_valid_status = record.status == '40'

            if is_active_within_window and is_valid_status:
                if record.sale_price < lowest_price:
                    lowest_price = record.sale_price
                    best_price_valid_from = record.promotion_start_date
                    best_price_valid_to = record.promotion_end_date
                    is_promo = True

        if lowest_price < 0:
            return LowestPriceResult(
                article_number=article_number,
                lowest_price=Decimal('0.00'),
                is_promo=False,
                valid_from=today,
                valid_to=today
            )

        return LowestPriceResult(
            article_number=article_number,
            lowest_price=lowest_price,
            is_promo=is_promo,
            valid_from=best_price_valid_from,
            valid_to=best_price_valid_to
        )


    def calculate_all_lowest_prices(self, today: date) -> List[LowestPriceResult]:
        """
        Calculates lowest price for all items in the dataset

        Args:
            today (date): _description_

        Returns:
            List[LowestPriceResult]: _description_
        """
        results: List[LowestPriceResult] = []

        for article_number in self.get_all_article_numbers():
            result = self.calculate_lowest_price_x_days(article_number, today)
            results.append(result)

        return results