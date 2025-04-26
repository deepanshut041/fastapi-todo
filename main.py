import uvicorn
from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager
from core.db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection
    db.init()
    print("Database connection initialized")

    yield  # Yield control to the application

    # Dispose of the database connection
    await db._engine.dispose()
    print("Database connection disposed")

# Create the FastAPI app with a lifespan
app = FastAPI(
    title="FastAPI Todo App",  # Set the name of the app for Swagger docs
    lifespan=lifespan,
)

v1_router = APIRouter(prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(v1_router)