import io
import pytest
from app.utils.processor import stream_and_aggregate, create_summary_csv

def test_stream_and_aggregate():
    # Create test CSV data
    csv_data = b"""Department Name,Date,Number of Sales
Electronics,2023-08-01,100
Clothing,2023-08-01,200
Electronics,2023-08-02,150
"""
    file = io.BytesIO(csv_data)

    result, metrics = stream_and_aggregate(file)

    assert result == {
        "Electronics": 250,
        "Clothing": 200
    }
    assert metrics['total_rows_processed'] == 3
    assert metrics['total_departments'] == 2
    assert "processing_time_seconds" in metrics
    assert "completed_at" in metrics

def test_create_summary_csv():
    department_totals = {
        "Electronics": 250,
        "Clothing": 200
    }
    output = create_summary_csv(department_totals)
    content = output.getvalue().splitlines()

    assert content[0] == "Department Name,Total Number of Sales"
    assert "Electronics,250" in content
    assert "Clothing,200" in content
