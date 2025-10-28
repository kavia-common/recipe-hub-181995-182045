from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

if TYPE_CHECKING:  # Only for type checkers to avoid runtime circular import
    from .recipe import Recipe


class Ingredient(Base):
    """ORM model for an ingredient belonging to a recipe."""
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True, nullable=False)

    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients", lazy="joined")
