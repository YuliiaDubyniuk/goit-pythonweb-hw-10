from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth import (
    ALGORITHM,
    SECRET_KEY,
    Hash,
    create_access_token,
)
from services.email import send_email


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: Request,
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

    await send_email(
        user.email,
        user.username,
        str(request.base_url).rstrip("/"),
    )

    return user


@router.get("/verify-email/{token}")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.verified:
        return {"message": "Email already verified"}

    user.verified = True

    db.commit()

    return {"message": "Email successfully verified"}


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
