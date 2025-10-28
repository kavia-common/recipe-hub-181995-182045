from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

if TYPE_CHECKING:
    from .recipe import Recipe


class Tag(Base):
    """ORM model for a tag used to categorize recipes."""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # Relationships
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="recipe_tags",
        back_populates="tags",
        lazy="selectin",
    )
