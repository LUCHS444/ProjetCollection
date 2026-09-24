from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.item import Item
from app.schemas.item import ItemRead, ItemList

router = APIRouter(prefix="/items", tags=["Catalogue"])


@router.get("", response_model=ItemList, summary="Lister/rechercher les recettes")
async def list_items(
    q: Optional[str] = Query(default=None, min_length=2, description="Recherche par mot-clé (titre)"),
    categorie: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=12, ge=1, le=50),
    session: AsyncSession = Depends(get_session),
):
    statement = select(Item)

    if q:
        statement = statement.where(Item.titre.ilike(f"%{q}%"))
    if categorie:
        statement = statement.where(Item.categorie == categorie)

    count_statement = select(func.count()).select_from(statement.subquery())
    total = (await session.exec(count_statement)).one()

    statement = statement.offset((page - 1) * limit).limit(limit)
    results = (await session.exec(statement)).all()

    return ItemList(total=total, page=page, limit=limit, results=results)


@router.get("/{item_id}", response_model=ItemRead, summary="Détail d'une recette")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item introuvable")
    return item