from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class RecipeTag(Base):
    """Association table mapping recipes to tags (many-to-many)."""
    __tablename__ = "recipe_tags"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
