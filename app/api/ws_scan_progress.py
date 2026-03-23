from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from urllib.parse import parse_qs
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models.dependencies import engine, SessionLocal
from app.services.db.models import image
from app.models.user import User
from app.utils.jwt import SECRET_KEY, ALGORITHM

router = APIRouter()

# Close code for auth failure (custom range 4000-4999)
WS_CLOSE_UNAUTHORIZED = 4001


def _get_user_from_token(token: str) -> User | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        db = SessionLocal()
        try:
            return db.query(User).filter(User.id == int(user_id)).first()
        finally:
            db.close()
    except (JWTError, ValueError):
        return None


@router.websocket("/ws/scan/{scan_id}")
async def scan_progress_socket(websocket: WebSocket, scan_id: str):
    # Accept first so the handshake completes; then validate token
    await websocket.accept()

    query_string = websocket.scope.get("query_string", "")
    params = parse_qs(query_string)
    token = (params.get("token") or [None])[0]
    current_user = _get_user_from_token(token) if token else None

    if current_user is None:
        await websocket.send_json({"error": "Unauthorized", "detail": "Invalid or missing token"})
        await websocket.close(code=WS_CLOSE_UNAUTHORIZED)
        return

    db = Session(bind=engine)
    try:
        while True:
            record = db.query(image).filter(image.image_id == scan_id).first()
            if record:
                db.refresh(record)
                data = json.loads(record.image_content)
                await websocket.send_json(data)
                if data.get("status") == "COMPLETED":
                    break
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
    finally:
        db.close()
