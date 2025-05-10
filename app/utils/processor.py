from io import StringIO, BytesIO, TextIOWrapper
from typing import Dict, Tuple
from datetime import datetime
import csv
import time
import uuid


def summarize_row(entry: dict, totals: Dict[str, int]):
    """Aggregate sales count from a row into the department total."""
    try:
        department = entry['Department Name']
        count = int(entry['Number of Sales'])
        totals[department] = totals.get(department, 0) + count
    except (ValueError, KeyError):
        # Ignore bad data rows
        pass

def create_summary_csv(totals: Dict[str, int]) -> StringIO:
    """Generate a CSV from the department sales summary."""
    output_buffer = StringIO()
    csv_writer = csv.writer(output_buffer)
    csv_writer.writerow(['Department Name', 'Total Number of Sales'])
    
    for department, count in totals.items():
        csv_writer.writerow([department, count])
    
    output_buffer.seek(0)
    return output_buffer

def create_unique_filename() -> str:
    """Generate a unique result filename using a time-based UUID."""
    return f"summary_{uuid.uuid1()}.csv"

def stream_and_aggregate(csv_stream: BytesIO) -> Tuple[Dict[str, int], dict]:
    """
    Stream a CSV file and compute aggregate sales by department.
    """
    start = time.time()
    row_count = 0
    department_totals: Dict[str, int] = {}

    csv_stream.seek(0)
    reader = csv.DictReader(TextIOWrapper(csv_stream, encoding='utf-8'),
                            fieldnames=['Department Name', 'Date', 'Number of Sales'])

    try:
        initial = next(reader)
        if initial['Department Name'] != 'Department Name':
            summarize_row(initial, department_totals)
            row_count += 1
    except StopIteration:
        pass

    for entry in reader:
        summarize_row(entry, department_totals)
        row_count += 1

    metrics = {
        'processing_time_seconds': time.time() - start,
        'total_rows_processed': row_count,
        'total_departments': len(department_totals),
        'completed_at': datetime.utcnow().isoformat()
    }

    return department_totals, metrics
