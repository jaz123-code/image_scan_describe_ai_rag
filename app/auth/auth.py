from fastapi import Depends, HTTPException, Header, Query
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.dependencies import get_db
from app.utils.jwt import SECRET_KEY, ALGORITHM


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user_ws(
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")