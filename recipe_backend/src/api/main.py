from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from .db import init_db, get_db
from .schemas import RecipeCreate, RecipeRead, RecipeUpdate
from .crud import create_recipe, list_recipes, get_recipe, update_recipe, delete_recipe

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


# PUBLIC_INTERFACE
@app.post("/recipes", response_model=RecipeRead, tags=["Recipes"], summary="Create recipe", description="Create a new recipe with ingredients and tags.")
def api_create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    """Create a recipe."""
    return create_recipe(db, payload)


# PUBLIC_INTERFACE
@app.get("/recipes", response_model=List[RecipeRead], tags=["Recipes"], summary="List recipes", description="List recipes, optionally filtering by a search query.")
def api_list_recipes(q: Optional[str] = Query(None, description="Search term for title/description"), db: Session = Depends(get_db)):
    """List recipes with optional search filter."""
    return list_recipes(db, q=q)


# PUBLIC_INTERFACE
@app.get("/recipes/{recipe_id}", response_model=RecipeRead, tags=["Recipes"], summary="Get recipe", description="Get a single recipe by ID.")
def api_get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get recipe by ID."""
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# PUBLIC_INTERFACE
@app.put("/recipes/{recipe_id}", response_model=RecipeRead, tags=["Recipes"], summary="Update recipe", description="Update a recipe and optionally replace ingredients and tags.")
def api_update_recipe(recipe_id: int, payload: RecipeUpdate, db: Session = Depends(get_db)):
    """Update a recipe."""
    recipe = update_recipe(db, recipe_id, payload)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# PUBLIC_INTERFACE
@app.delete("/recipes/{recipe_id}", response_model=dict, tags=["Recipes"], summary="Delete recipe", description="Delete a recipe by ID.")
def api_delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe."""
    ok = delete_recipe(db, recipe_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"status": "deleted", "id": recipe_id}
