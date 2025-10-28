"""
CRUD service layer for recipes, ingredients, and tags.
"""

from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .models.recipe import Recipe
from .models.ingredient import Ingredient
from .models.tag import Tag
from .schemas import RecipeCreate, RecipeUpdate


def _get_or_create_tags(db: Session, tag_names: List[str]) -> List[Tag]:
    """Return Tag objects for the provided names, creating any that don't exist."""
    cleaned = [t.strip() for t in tag_names if t and t.strip()]
    if not cleaned:
        return []
    existing = db.execute(select(Tag).where(Tag.name.in_(cleaned))).scalars().all()
    existing_names = {t.name for t in existing}
    to_create = [Tag(name=name) for name in cleaned if name not in existing_names]
    for t in to_create:
        db.add(t)
    if to_create:
        db.flush()  # Assign IDs
    return existing + to_create


# PUBLIC_INTERFACE
def create_recipe(db: Session, payload: RecipeCreate) -> Recipe:
    """Create a Recipe with ingredients and tags."""
    recipe = Recipe(
        title=payload.title,
        description=payload.description,
        instructions=payload.instructions,
    )
    db.add(recipe)
    db.flush()  # ensure recipe.id

    # Ingredients
    for ing in payload.ingredients:
        db.add(Ingredient(name=ing.name, quantity=ing.quantity, recipe_id=recipe.id))

    # Tags
    tags = _get_or_create_tags(db, payload.tags)
    recipe.tags = tags

    db.commit()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def list_recipes(db: Session, q: Optional[str] = None) -> List[Recipe]:
    """List recipes, optionally filtered by a search query in title/description."""
    stmt = select(Recipe)
    if q:
        like = f"%{q}%"
        from sqlalchemy import or_
        stmt = stmt.where(or_(Recipe.title.ilike(like), Recipe.description.ilike(like)))
    return db.execute(stmt).scalars().unique().all()


# PUBLIC_INTERFACE
def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
    """Fetch a single recipe by ID."""
    return db.get(Recipe, recipe_id)


# PUBLIC_INTERFACE
def update_recipe(db: Session, recipe_id: int, payload: RecipeUpdate) -> Optional[Recipe]:
    """Update a recipe and optionally replace ingredients/tags."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        return None

    if payload.title is not None:
        recipe.title = payload.title
    if payload.description is not None:
        recipe.description = payload.description
    if payload.instructions is not None:
        recipe.instructions = payload.instructions

    # Replace ingredients if provided
    if payload.ingredients is not None:
        db.execute(delete(Ingredient).where(Ingredient.recipe_id == recipe.id))
        for ing in payload.ingredients:
            db.add(Ingredient(name=ing.name, quantity=ing.quantity, recipe_id=recipe.id))

    # Replace tags if provided
    if payload.tags is not None:
        recipe.tags = _get_or_create_tags(db, payload.tags)

    db.commit()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def delete_recipe(db: Session, recipe_id: int) -> bool:
    """Delete a recipe by ID. Returns True if deleted, False if not found."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        return False
    db.delete(recipe)
    db.commit()
    return True
