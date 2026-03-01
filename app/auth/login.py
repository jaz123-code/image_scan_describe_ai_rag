from app.utils.security import verify_password
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt import create_access_token
from app.models.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password, user.hashed_password):
        return {"error": "Invalid credentials"}
    
    token=create_access_token({"sub": user.id})
    return {"access_token": token}