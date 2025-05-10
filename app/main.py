from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.sales_routes import router as sales_router

app = FastAPI(
    title="Sales Data Processor API",
    description="API for processing large CSV files with sales data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sales_router, prefix="/api/v1/sales", tags=["sales"])

@app.get("/")
def health_check():
    return {"status": "healthy"}