import io
import pytest
from fastapi import UploadFile
from app.services.sales_controller import process_uploaded_csv

@pytest.mark.asyncio
async def test_process_uploaded_csv():
    # Simulate a CSV upload
    csv_content = b"""Department Name,Date,Number of Sales
Electronics,2023-08-01,100
Clothing,2023-08-01,200
Electronics,2023-08-02,150
"""
    file_stream = io.BytesIO(csv_content)
    upload = UploadFile(filename="test.csv", file=file_stream)

    # Call the controller function directly (without background processing)
    response = await process_uploaded_csv(upload)

    # Assertions
    assert response.message == "Processing completed successfully"
    assert "download" in response.download_link
    assert response.metrics["total_rows_processed"] == 3
    assert response.metrics["total_departments"] == 2
