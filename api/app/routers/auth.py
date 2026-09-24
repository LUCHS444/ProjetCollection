from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Créer un compte")
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.exec(select(User).where(User.email == data.email))
    if existing.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email déjà utilisé")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=Token, summary="Se connecter")
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()

    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe invalide")

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead, summary="Voir mon profil")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user