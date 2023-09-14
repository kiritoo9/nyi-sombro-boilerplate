import os
import jwt
from src.configs.database import DB_SESSION
from src.models.user import User
from src.configs.config import settings
from src.businesses.user import getUserById

async def verifyToken(token) -> dict:
    if token is None:
        return { "message": "Missing authorization header", "code": 401 }

    token = token[7:]
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except Exception as e:
        return { "message": "Token is not valid", "code": 401 }

    # Check existing user
    db = DB_SESSION()
    user = await getUserById(db, decoded.get("id"))
    db.close()
    if user is None:
        return { "message": "User is not found, probably token is expired already", "code": 401 }

    return { "message": "You are authenticated", "code": 200 }