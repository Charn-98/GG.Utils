import pathlib
from decimal import Decimal
from fastapi import FastAPI
from src.repositories.csv_repository import CSVRepository
from src.repositories.interface import IPriceRepository
from src.services.price_service import PriceService
from src.api.dependencies import get_price_service
import uvicorn
from src.api.router import router

DATA_DIRECTORY = pathlib.Path(__file__).parent / "data"
SELLING_PRICES_FILE = f"{DATA_DIRECTORY}/verkoopprijzen.csv"
PROMOTIONS_FILE = f"{DATA_DIRECTORY}/promoties.csv"

#not sure about this, apparently it is a good practise to set Decimal context to be globally consistent
Decimal.setcontext(Decimal('0') + Decimal('1e-2'))

#initialize api
app = FastAPI(
    title="Gall & Gall microservice",
    version="1.0.0",
    description="Calculates the lowest price for article(s)"
)

#initialize repository and trigger the iniital data load to resemble cache
price_repository: IPriceRepository = CSVRepository(
    selling_price_file=SELLING_PRICES_FILE,
    promotion_price_file=PROMOTIONS_FILE
)

#initialize service, inject repository
price_service = PriceService(repository=price_repository)
#inject the service instance into router dependency. This is to allow the service to be singleton, but in real-world would be a factory
app.dependency_overrides[get_price_service] = price_service

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    #run: uvicorn main:app --reload
    print(f"Starting service. Data files expected at: {DATA_DIRECTORY.resolve()}")
    uvicorn.run(app, host="0.0.0.0", port=8000)