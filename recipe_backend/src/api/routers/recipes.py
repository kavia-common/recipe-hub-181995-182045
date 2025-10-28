from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import RecipeCreate, RecipeRead, RecipeUpdate
from ..crud import (
    create_recipe as svc_create_recipe,
    list_recipes as svc_list_recipes,
    get_recipe as svc_get_recipe,
    update_recipe as svc_update_recipe,
    delete_recipe as svc_delete_recipe,
)
from ..models.recipe import Recipe
from ..models.tag import Tag

router = APIRouter(prefix="/recipes", tags=["Recipes"])


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=RecipeRead,
    summary="Create recipe",
    description="Create a new recipe with ingredients and tags.",
)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)) -> RecipeRead:
    """Create a recipe with ingredients and tags and return the created recipe."""
    return svc_create_recipe(db, payload)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[RecipeRead],
    summary="List recipes",
    description="List recipes, optionally filtering by a search query, tag name, and with pagination.",
)
def list_recipes(
    q: Optional[str] = Query(None, description="Search term for title/description"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    skip: int = Query(0, ge=0, description="Number of records to skip (pagination)"),
    limit: int = Query(50, ge=1, le=100, description="Max records to return (pagination)"),
    db: Session = Depends(get_db),
) -> List[RecipeRead]:
    """List recipes filtered by optional search and tag, with pagination."""
    # If only search query is used, re-use service function for simplicity (no pagination there).
    if tag is None and skip == 0 and limit == 50:
        return svc_list_recipes(db, q=q)

    # Build query with optional filters and pagination
    stmt = select(Recipe)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Recipe.title.ilike(like), Recipe.description.ilike(like)))
    if tag:
        # Filter recipes that have a tag with name == tag
        stmt = (
            stmt.join(Recipe.tags)
            .where(func.lower(Tag.name) == func.lower(tag))
        )
    stmt = stmt.offset(skip).limit(limit)
    results = db.execute(stmt).scalars().unique().all()
    return results


# PUBLIC_INTERFACE
@router.get(
    "/{recipe_id}",
    response_model=RecipeRead,
    summary="Get recipe",
    description="Get a single recipe by ID.",
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> RecipeRead:
    """Fetch a single recipe by ID or return 404 if not found."""
    recipe = svc_get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# PUBLIC_INTERFACE
@router.put(
    "/{recipe_id}",
    response_model=RecipeRead,
    summary="Update recipe",
    description="Update a recipe and optionally replace ingredients and tags.",
)
def update_recipe(recipe_id: int, payload: RecipeUpdate, db: Session = Depends(get_db)) -> RecipeRead:
    """Update a recipe by ID or return 404 if not found."""
    recipe = svc_update_recipe(db, recipe_id, payload)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# PUBLIC_INTERFACE
@router.delete(
    "/{recipe_id}",
    response_model=dict,
    summary="Delete recipe",
    description="Delete a recipe by ID.",
)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)) -> dict:
    """Delete a recipe by ID or return 404 if not found."""
    ok = svc_delete_recipe(db, recipe_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"status": "deleted", "id": recipe_id}
