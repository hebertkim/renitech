# app/routes/profile.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserProfileResponse, UserProfileUpdate
from app.security import get_current_user, hash_password

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.put("/me")
def update_my_profile(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.name = data.name
    current_user.email = data.email

    if data.avatar:
        current_user.avatar = data.avatar

    if data.password:
        current_user.password_hash = hash_password(data.password)

    db.commit()
    return {"success": True}
