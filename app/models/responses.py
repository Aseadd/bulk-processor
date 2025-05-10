from pydantic import BaseModel
from typing import Optional
from app.models.schemas import ProcessingMetrics

class FileUploadResponse(BaseModel):
    status: str
    message: Optional[str] = None
    download_link: Optional[str] = None
    metrics: Optional[ProcessingMetrics] = None