####goal: load csv files once on startup so that the get & getall methods can read from memory.
import csv
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, date
import math
import os
from src.repositories.interface import IPriceRepository
from src.models.promotion_record import PromotionRecord
from src.models.selling_record import SellingRecord
from src.models.dto.paginated_result import PaginatedResult

class CSVRepository(IPriceRepository):
    """
    All data is loaded into memory on startup for quick lookups.
    This is hopefully mimicking a database cache layer

    Args:
        IPriceRepository (_type_): _description_
    """

    _SELLING_PRICE_HEADERS = [
        "ArtikelNummer", "ArtikelDatum", "IngangsDatumPrijs",
        "EindDatumPrijs", "Prijs"
    ]

    _PROMOTION_HEADERS = [
        "ActiePeriode", "PromotieNummer", "ArtikelNummer", "ArtikelDatum",
        "PromotieOmschrijving", "StartDatumPromotie", "EindDatumPromotie",
        "Status", "VanPrijs", "VoorPrijs"
    ]

    def __init__(self, selling_price_file: str, promotion_price_file: str):
        super().__init__()
        self._selling_prices: List[SellingRecord] = []
        self._promotions: List[PromotionRecord] = []

        self._load_data(selling_price_file, promotion_price_file)

    ########################################
    #          PRIVATE METHODS
    ########################################
    def _parse_date(Self, date_str: str, format_hints: List[str]) -> Optional[datetime.date]:
        """
        Parse date string using multiple formats, also handles cases where date is null.

        Args:
            Self (_type_): _description_
            date_str (str): _description_
            format_hints (List[str]): _description_

        Returns:
            Optional[datetime.date]: _description_
        """
        if not date_str or date_str.lower() in ('null', 'n/a', 'na'):
            return None

        for fmt in format_hints:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Could not parse date string: {date_str}")

    def _load_selling_prices(self, file_path: str):
        """
        Loads and parses regular selling price data

        Args:
            Self (_type_): _description_
            file_path (str): _description_
        """
        if not os.path.exists(file_path):
            print(f"Warning: Selling prices file not found at {file_path}")
            return

        DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%y', '%d/%m/%Y']

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, fieldnames = self._SELLING_PRICE_HEADERS)
            next(reader) #skip headers

            for i, row in enumerate(reader):
                try:
                    price_start_date = self._parse_date(row['IngangsDatumPrijs'], DATE_FORMATS)
                    price_end_date = self._parse_date(row['EindDatumPrijs'], DATE_FORMATS) or date(9999, 12, 31)
                    article_date = self._parse_date(row['ArtikelDatum'], DATE_FORMATS)

                    #end date can be null
                    if not all([article_date, price_start_date]):
                         raise ValueError("Missing date fields.")

                    record = SellingRecord(
                        article_number=row['ArtikelNummer'],
                        article_date=article_date,
                        price_start_date=price_start_date,
                        price_end_date=price_end_date,
                        price=Decimal(row['Prijs'])
                    )

                    self._selling_prices.append(record)
                except Exception as e:
                    print(f"Unexpected error: {e}")

            print("Successfully loaded selling price records.")

    def _load_promotion_prices(self, file_path: str):
        """
        Loads and parses promotion selling price data

        Args:
            Self (_type_): _description_
            file_path (str): _description_
        """
        if not os.path.exists(file_path):
            print(f"Warning: Promption prices file not found at {file_path}")
            return

        DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%y', '%d/%m/%Y']

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, fieldnames = self._PROMOTION_HEADERS)
            next(reader) #skip headers

            for i, row in enumerate(reader):
                try:
                    promption_start_date = self._parse_date(row['StartDatumPromotie'], DATE_FORMATS)
                    promption_end_date = self._parse_date(row['EindDatumPromotie'], DATE_FORMATS)
                    article_date = self._parse_date(row['ArtikelDatum'], DATE_FORMATS)

                    if not all([article_date, promption_start_date, promption_end_date]):
                         raise ValueError("Missing date fields.")

                    record = PromotionRecord(
                        article_number=row['ArtikelNummer'],
                        article_date=article_date,
                        promption_start_date=promption_start_date,
                        promption_end_date=promption_end_date,
                        price=Decimal(row['Prijs']),
                        campaign_period=row['ActiePeriode'],
                        promotion_number=row['PromotieNummer'],
                        promotion_description=row['PromotieOmschrijving'],
                        status=row['Status'],
                        original_price=Decimal(row['VanPrijs']),
                        sale_price=Decimal(row['VoorPrijs'])
                    )

                    self._promotions.append(record)
                except Exception as e:
                    print(f"Unexpected error: {e}")

            print("Successfully loaded promotional price records.")

    def _load_data(self, selling_prices_file: str, promotions_file: str):
        """Main entry point for data loading."""
        self._load_selling_prices(selling_prices_file)
        self._load_promotion_prices(promotions_file)


    ########################################
    #          INTERFACE IMPLEMENTATION
    ########################################
    def get_all_selling_prices(self) -> List[SellingRecord]:
        """Fetches all regular selling price records with pagination. Not paginated"""
        return self._selling_prices

    def get_all_promotions(self) -> List[PromotionRecord]:
        """Fetches all promotion records with pagination. Not paginated"""
        return self._promotions

    def get_selling_prices_by_item(self, item_number: str) -> List[SellingRecord]:
        """Fetches regular selling price records for a specific item number."""
        return [
            record for record in self._selling_prices
            if record.item_number == item_number
        ]

    def get_promotions_by_item(self, item_number: str) -> List[PromotionRecord]:
        """Fetches promotion records for a specific item number."""
        return [
            record for record in self._promotions
            if record.item_number == item_number
        ]
