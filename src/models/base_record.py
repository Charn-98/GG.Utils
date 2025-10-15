from datetime import date
from pydantic import BaseModel

class BaseRecord(BaseModel):
    article_number: str
    article_date: date

