from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from schemas.user import UserResponse
from services.auth import get_current_user
from database.db import get_db
from database.models import User
from services.cloudinary import upload_avatar

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)

@router.get(
    "/me",
    response_model=UserResponse,
    description="No more than 10 requests per minute",
)
@limiter.limit("10/minute")
async def me(
    request: Request,
    user: UserResponse = Depends(get_current_user),
):
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image",
        )
    
    avatar_url = upload_avatar(
        file,
        current_user.username,
    )

    current_user.avatar = avatar_url

    db.commit()
    db.refresh(current_user)

    return current_user
