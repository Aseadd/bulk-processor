from fastapi import BackgroundTasks, UploadFile
from typing import Dict, Tuple
from app.utils.processor import stream_and_aggregate, create_summary_csv, create_unique_filename
from app.utils.result import LocalFileStorage
from app.models.schemas import ProcessFileResponse
import io

file_storage = LocalFileStorage()

async def retrieve_processed_summary(summary_id: str):
    """Retrieve a processed sales summary CSV by its ID."""
    return await file_storage.get_file(summary_id)

async def process_uploaded_csv(uploaded_file: UploadFile, background: BackgroundTasks = None) -> ProcessFileResponse:
    """
    Handle the uploaded sales CSV and return a response with download details.
    Supports both immediate and background processing.
    """
    summary_file_id = create_unique_filename()
    file_content = await uploaded_file.read()

    if background:
        background.add_task(process_in_background, file_content, summary_file_id)
        return ProcessFileResponse(
            message="Processing started in the background",
            file_id=summary_file_id,
            download_link=file_storage.get_download_link(summary_file_id),
            metrics=None
        )
    else:
        file_buffer = io.BytesIO(file_content)
        department_summary, summary_metrics = stream_and_aggregate(file_buffer)
        result_csv = create_summary_csv(department_summary)
        await file_storage.save_file(summary_file_id, result_csv)
        return ProcessFileResponse(
            message="File processed successfully",
            file_id=summary_file_id,
            download_link=file_storage.get_download_link(summary_file_id),
            metrics=summary_metrics
        )

async def process_in_background(file_bytes: bytes, summary_file_id: str):
    """
    Background task to process the uploaded file and save the output.
    """
    stream_buffer = io.BytesIO(file_bytes)
    aggregated_data, metrics = stream_and_aggregate(stream_buffer)
    output_csv = create_summary_csv(aggregated_data)
    await file_storage.save_file(summary_file_id, output_csv)
