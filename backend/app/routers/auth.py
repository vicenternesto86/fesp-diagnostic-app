"""
Authentication Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, Token, UserResponse
from app.utils.auth import verify_password, create_access_token, get_current_user, get_password_hash
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user info
    """
    return current_user


@router.get("/reset-passwords-temp")
def reset_passwords_temp(db: Session = Depends(get_db)):
    """
    TEMPORARY: Reset all passwords to Fesp_SNSP_2026
    DELETE THIS ENDPOINT AFTER FIRST USE!
    """
    new_hash = get_password_hash("Fesp_SNSP_2026")
    users = db.query(User).all()
    for user in users:
        user.password_hash = new_hash
    db.commit()
    return {"message": f"Reset passwords for {len(users)} users", "hash_preview": new_hash[:30] + "..."}
