from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.entry import Entry


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(index=True, nullable=False)
    categorie: str = Field(index=True, nullable=False)
    description: str = Field(nullable=False)
    image_url: Optional[str] = Field(default=None)

    # Champs spécifiques à l'univers "Cuisine / Recettes"
    temps_preparation: int = Field(nullable=False)  # en minutes
    difficulte: str = Field(nullable=False)          # "facile" | "moyen" | "difficile"
    type_plat: str = Field(nullable=False)           # "entree" | "plat" | "dessert" | ...

    entries: List["Entry"] = Relationship(back_populates="item")