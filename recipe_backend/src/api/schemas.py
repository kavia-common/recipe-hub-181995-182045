"""
Pydantic schemas for request/response validation and serialization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(..., description="Name of the ingredient")
    quantity: Optional[str] = Field(None, description="Quantity or measurement for the ingredient")


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int = Field(..., description="Ingredient ID")

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    name: str = Field(..., description="Unique tag name")


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int = Field(..., description="Tag ID")

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(None, description="Recipe description")
    instructions: Optional[str] = Field(None, description="Cooking instructions")


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate] = Field(default_factory=list, description="List of ingredients")
    tags: List[str] = Field(default_factory=list, description="List of tag names to associate")


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Recipe title")
    description: Optional[str] = Field(None, description="Recipe description")
    instructions: Optional[str] = Field(None, description="Cooking instructions")
    ingredients: Optional[List[IngredientCreate]] = Field(None, description="Replace ingredients with this list")
    tags: Optional[List[str]] = Field(None, description="Replace tags with this list of tag names")


class RecipeRead(RecipeBase):
    id: int = Field(..., description="Recipe ID")
    ingredients: List[IngredientRead] = Field(default_factory=list, description="Ingredients for the recipe")
    tags: List[TagRead] = Field(default_factory=list, description="Tags associated with the recipe")

    class Config:
        from_attributes = True
