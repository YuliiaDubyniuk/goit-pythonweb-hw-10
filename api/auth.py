from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth import Hash, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = Hash().get_password_hash(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        verified=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )
    if not Hash().verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    access_token = await create_access_token(
        data={"sub": user.username},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }