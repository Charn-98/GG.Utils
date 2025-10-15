from fastapi import APIRouter, Depends, Query, HTTPException
from src.models.dto.lowest_price_result import LowestPriceResult
from src.models.dto.paginated_result import PaginatedResult
from src.services.price_service import PriceService
from src.api.dependencies import get_price_service
from decimal import Decimal
from datetime import date
from typing import List

router = APIRouter()
@router.get(
    "/lowest-price/{article_number}",
    response_model=LowestPriceResult,
    summary="Get the lowest price for a specific item in the last 30 days"
)

def get_lowest_price_for_item(
    article_number: str,
    price_service: PriceService = Depends(get_price_service),
    today: date = Query(default=date.today())
):
    """
    Fetches the lowest price and related information for the given item
    over the 30 days preceding the 'today' date.
    """
    result = price_service.calculate_lowest_price_x_days(article_number, today)

    if result.lowest_price == Decimal('0.00') and article_number not in price_service.get_all_article_numbers():
         raise HTTPException(status_code=404, detail=f"Item number '{article_number}' not found in data history.")

    return result

@router.get(
    "/lowest-prices/all",
    response_model=PaginatedResult[LowestPriceResult],
    summary="Get lowest prices for all items with pagination"
)
def get_all_lowest_prices(
    price_service: PriceService = Depends(get_price_service),
    today: date = Query(default=date.today()),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100)
):
    """
    Calculates the 30-day lowest price for all unique items in the dataset
    and returns the results paginated.
    """
    all_results: List[LowestPriceResult] = price_service.calculate_all_lowest_prices(today)

    all_results.sort(key=lambda x: x.article_number)
    total_count = len(all_results)

    start_index = (page - 1) * size
    end_index = start_index + size

    paginated_data = all_results[start_index:end_index]

    return PaginatedResult(
        data=paginated_data,
        total_count=total_count,
        page_number=page,
        page_size=size
    )