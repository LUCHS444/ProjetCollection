from typing import Literal, Optional
from pydantic import BaseModel

Difficulte = Literal["facile", "moyen", "difficile"]
TypePlat = Literal["entree", "plat", "dessert", "boisson", "autre"]


class ItemRead(BaseModel):
    id: int
    titre: str
    categorie: str
    description: str
    image_url: Optional[str] = None
    temps_preparation: int
    difficulte: Difficulte
    type_plat: TypePlat

    class Config:
        from_attributes = True


class ItemList(BaseModel):
    total: int
    page: int
    limit: int
    results: list[ItemRead]