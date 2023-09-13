import os
import bcrypt
import jwt
from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.configs.database import get_db
from src.configs.config import settings
from src.businesses.user import getUserByEmail

class Body(BaseModel):
    email: str | None = Field(title="Email cannot be empty")
    password: str | None = Field(title="Password cannot be empty")

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

@router.post("/login", status_code=201)
async def login(
    response: Response,
    body: Body,
    db: Session = Depends(get_db)
):
    try:
        data = await getUserByEmail(db, body.email)
        if data is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { "message": "User is not found" }

        # Check hash password
        encoded_password = body.password.encode("utf-8")
        if bcrypt.checkpw(encoded_password, data.get("password").encode("utf-8")) is False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return { "message": "Email and password does not match" }

        # Genearate Token
        payloads = {
            "id": str(data.get("id")),
            "email": data.get("email"),
            "fullname": data.get("fullname"),
            "role": "admin" # static data
        }
        encoded_jwt = jwt.encode(payloads, settings.SECRET_KEY, algorithm="HS256")

        # Generate token and send response
        return {
            "message": "You are authenticated",
            "access_token": encoded_jwt
        }
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": str(e)
        }