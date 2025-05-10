from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from app.services.sales_controller import process_uploaded_csv, retrieve_processed_summary
from app.models.schemas import ProcessFileResponse
from app.utils.result import LocalFileStorage, LOCAL_STORAGE_PATH
import os

router = APIRouter()
file_storage = LocalFileStorage()

@router.post("/upload", response_model=ProcessFileResponse)
async def upload_csv_file(
    task_queue: BackgroundTasks,
    upload: UploadFile = File(...),
    run_in_background: bool = False
):
    """
    Upload a CSV file for processing.

    Parameters:
    - upload: The uploaded CSV file
    - run_in_background: Whether to process the file asynchronously

    Returns:
    - File metadata and a download link
    """
    if not upload.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    return await process_uploaded_csv(upload, task_queue if run_in_background else None)

@router.get("/results/{result_id}")
async def download_processed_file(result_id: str):
    """
    Download a processed CSV file by result ID.

    Parameters:
    - result_id: The unique ID of the processed file

    Returns:
    - FileResponse with the processed CSV
    """
    if not file_storage.file_exists(result_id):
        raise HTTPException(status_code=404, detail="Result file not found")

    result_path = os.path.join(LOCAL_STORAGE_PATH, result_id)
    return FileResponse(
        path=result_path,
        media_type="text/csv",
        filename=f"aggregated_sales_{result_id}"
    )
