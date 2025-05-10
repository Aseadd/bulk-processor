# 🧪 Bulk Sales Data Processor API

High-performance API that processes large CSV files containing departmental sales

## Features

- Process large CSV files efficiently using streaming/chunked reading
- Aggregate sales data by department
- Background processing for large files
- Downloadable results
- Metrics collection

## 🛠️ Setup Instructions

1.  Clone the repository:
    ```bash
    git clone https://github.com/Aseadd/bulk-processor
    cd bulk-processor
    ```
2.  Activate the virtual environment:
    - Windows: `venv\Scripts\activate`
    - Unix/MacOS: `source venv/bin/activate`
3.  Install dependencies: `pip install -r requirements.txt`

---

## Running the Application

- uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/sales/process` - Upload a CSV file for processing
  - Parameters:
    - `file`: The CSV file to upload
    - `async_processing`: Set to true for background processing
- `GET /api/v1/sales/download/{file_id}` - Download a processed file

## Using Docker

1. Clone the repository
2. docker compose up --build app app
   The API will be available at `http://localhost:8000`

## 🧪 Testing

Run tests with:

pytest

## 🧱 Algorithm Explanation

The solution processes CSV files in chunks to handle large files efficiently:

1. **Streaming Processing**: The CSV file is read line by line, never loading the entire file into memory.
2. **Incremental Aggregation**: Sales numbers are aggregated by department as each row is processed.
3. **Memory Efficiency**: Only the aggregated totals (department name → total sales) are kept in memory, not the original data.
4. **Background Processing**: Large files can be processed asynchronously to avoid blocking the API.

### 🧱 Computational Complexity

- Time Complexity: O(n) where n is the number of rows in the CSV
- Space Complexity: O(m) where m is the number of unique departments (typically much smaller than n)

## 👥 Author <a name="author"></a>

Addis Tsega

- GitHub: [Aseadd](https://github.com/Aseadd)
- Twitter: [@AdaTsega](https://twitter.com/AdaTsega)
- LinkedIn: [addis-tsega](https://www.linkedin.com/in/addis-tsega/)

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## 📝 License <a name="license"></a>

This project is [MIT](./MIT.md) licensed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
