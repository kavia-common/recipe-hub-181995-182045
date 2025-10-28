from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routers.recipes import router as recipes_router

openapi_tags = [
    {"name": "Health", "description": "Service health and info"},
    {"name": "Recipes", "description": "CRUD operations for managing recipes"},
]

app = FastAPI(
    title="Recipe Hub Backend",
    description="Backend API for Recipe Hub. Provides CRUD for recipes with SQLite persistence.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()


@app.get("/", tags=["Health"], summary="Health Check", description="Check service health")
def health_check():
    """Return service health information."""
    return {"message": "Healthy"}


# Mount routers
app.include_router(recipes_router)
