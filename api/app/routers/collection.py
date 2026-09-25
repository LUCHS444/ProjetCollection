from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.entry import Entry
from app.models.item import Item
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryUpdate, EntryRead, StatsRead
from app.dependencies.auth import get_current_user
from sqlmodel import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/me", tags=["Collection personnelle"])


@router.get("/collection", response_model=list[EntryRead], summary="Lister ma collection")
async def list_my_collection(
    statut: Optional[str] = Query(default=None),
    tri: Optional[str] = Query(default=None, description="'date' ou 'note'"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    statement = (
        select(Entry)
        .where(Entry.user_id == current_user.id)
        .options(selectinload(Entry.item))
    )

    if statut:
        statement = statement.where(Entry.statut == statut)

    if tri == "note":
        statement = statement.order_by(Entry.note.desc())
    else:
        statement = statement.order_by(Entry.date_ajout.desc())

    result = await session.exec(statement)
    return result.all()


@router.post("/collection", response_model=EntryRead, status_code=status.HTTP_201_CREATED, summary="Ajouter un élément à ma collection")
async def add_to_collection(
    data: EntryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    item = await session.get(Item, data.item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item introuvable")

    existing = await session.exec(
        select(Entry).where(Entry.user_id == current_user.id, Entry.item_id == data.item_id)
    )
    if existing.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cet élément est déjà dans votre collection")

    entry = Entry(
        user_id=current_user.id,
        item_id=data.item_id,
        statut=data.statut,
        note=data.note,
        commentaire=data.commentaire,
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry, attribute_names=["item"])
    return entry


async def _get_owned_entry(entry_id: int, current_user: User, session: AsyncSession) -> Entry:
    entry = await session.get(Entry, entry_id)
    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable")
    return entry


@router.patch("/collection/{entry_id}", response_model=EntryRead, summary="Modifier une entrée")
async def update_entry(
    entry_id: int,
    data: EntryUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    entry = await _get_owned_entry(entry_id, current_user, session)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entry, key, value)

    session.add(entry)
    await session.commit()
    await session.refresh(entry, attribute_names=["item"])
    return entry


@router.delete("/collection/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une entrée")
async def delete_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    entry = await _get_owned_entry(entry_id, current_user, session)
    await session.delete(entry)
    await session.commit()


@router.get("/stats", response_model=StatsRead, summary="Mes statistiques")
async def my_stats(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(Entry).where(Entry.user_id == current_user.id))
    entries = result.all()

    total = len(entries)
    par_statut: dict[str, int] = {}
    for e in entries:
        par_statut[e.statut] = par_statut.get(e.statut, 0) + 1

    notes = [e.note for e in entries if e.note is not None]
    note_moyenne = round(sum(notes) / len(notes), 2) if notes else None

    return StatsRead(total=total, par_statut=par_statut, note_moyenne=note_moyenne)