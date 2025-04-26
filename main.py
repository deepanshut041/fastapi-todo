import uvicorn
from fastapi import APIRouter, FastAPI


app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(v1_router)