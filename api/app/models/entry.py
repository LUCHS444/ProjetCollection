from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.item import Item


class Entry(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uq_user_item"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    statut: str = Field(nullable=False)  # "a_decouvrir" | "en_cours" | "termine"
    note: Optional[int] = Field(default=None, ge=1, le=5)
    commentaire: Optional[str] = Field(default=None)
    date_ajout: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    item_id: int = Field(foreign_key="item.id", nullable=False)

    user: "User" = Relationship(back_populates="entries")
    item: "Item" = Relationship(back_populates="entries")