from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .tag import Tag


class Recipe(Base):
    """ORM model for a recipe."""
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="recipe_tags",
        back_populates="recipes",
        lazy="selectin",
    )
