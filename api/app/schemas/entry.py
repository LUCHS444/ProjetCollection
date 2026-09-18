from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

from app.schemas.item import ItemRead

Statut = Literal["a_decouvrir", "en_cours", "termine"]


class EntryCreate(BaseModel):
    item_id: int
    statut: Statut
    note: Optional[int] = Field(default=None, ge=1, le=5)
    commentaire: Optional[str] = None


class EntryUpdate(BaseModel):
    statut: Optional[Statut] = None
    note: Optional[int] = Field(default=None, ge=1, le=5)
    commentaire: Optional[str] = None


class EntryRead(BaseModel):
    id: int
    statut: Statut
    note: Optional[int] = None
    commentaire: Optional[str] = None
    date_ajout: datetime
    item: ItemRead

    class Config:
        from_attributes = True


class StatsRead(BaseModel):
    total: int
    par_statut: dict[str, int]
    note_moyenne: Optional[float] = None