from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import process_router
from .services import mongodb_service
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongodb_service.connect()
    print("Connected to MongoDB")
    yield
    # Shutdown
    await mongodb_service.close()
    print("Closed MongoDB connection")


app = FastAPI(
    title="Data Processing Backend",
    description="Backend service for processing Excel files with MongoDB join and external API integration",
    version="1.0.0",
    lifespan=lifespan,
    redirect_slashes=False
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(health_router)
app.include_router(process_router)


@app.get("/")
async def root():
    return {
        "message": "Data Processing Backend API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
