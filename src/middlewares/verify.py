import os
import jwt
from sqlalchemy.orm import Session
from src.configs.config import settings
from src.businesses.user import getUserById

async def verifyToken():
    print("token called")
    # try:
    #     decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    # except Exception as e:
    #     return { "message": "Token is not valid", "status": False }

    # # Check existing user
    # user = await getUserById(db, decoded.get("id"))
    # if user is None:
    #     return { "message": "User is not found, probably token is expired already", "status": False }
    # else:
    #     return { "message": "You are authenticated", "status": True }