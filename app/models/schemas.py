from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class SalesData(BaseModel):
    department_name: str
    date: str
    number_of_sales: int

class ProcessFileResponse(BaseModel):
    message: str
    file_id: str
    download_link: str
    metrics: Optional[dict] = None
