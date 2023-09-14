import uuid
import math
import bcrypt
from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.configs.database import get_db
from src.businesses.user import getUserLists, getUserCount, getUserById, createUser, getUserByEmail, updateUser
from src.helpers.upload import upload

# Request body model
class Body(BaseModel):
    email: str | None = Field(title="Email cannot be empty", max_length=50, min_length=5)
    password: str | None = Field(default=None, min_length=6)
    fullname: str | None = Field(title="Fullname cannot be empty", min_length=1)
    photo: str | None = None

class BodyInsert(Body):
    password: str | None = Field(title="Password cannot be empty", min_length=6)

# Set up Route
router = APIRouter(
    prefix = "/user",
    tags = ["master.user"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def list(
    response: Response, # to change response status code
    db: Session = Depends(get_db), # database session
    page: int | None = 1, # query params -> &page
    limit: int | None = 10, # query params -> &limit
    keywords: str | None = None # query params -> &keywords
):
    try:
        # Get data from business
        data = await getUserLists(db, page, limit, keywords)
        totalPage = await getUserCount(db, limit, keywords)

        # Response
        return {
            "limit": limit,
            "currentPage": page,
            "totalPage": totalPage,
            "data": data
        }
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": str(e)
        }

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def detail(
    id, 
    response: Response,
    db: Session = Depends(get_db)
):
    data = await getUserById(db, id)
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": "Data is not found"
        }

    return data

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    response: Response,
    body: BodyInsert,
    db: Session = Depends(get_db)
):
    # Validate existing email
    user = await getUserByEmail(db, body.email)
    if user is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "Email is already taken, please try another one"
        }

    # Hash password
    encoded_password = body.password.encode("utf-8")
    body.password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode("utf-8")

    # Upload photo
    if body.photo is not None and body.photo != "":
        uploadResponse = await upload(body.photo, "users")
        if uploadResponse.get("uploaded") is False:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { "message": uploadResponse.get("message") }
        else:
            # Condition when upload file is success
            body.photo = uploadResponse.get("filename")

    # Create data
    data = {
        "id": str(uuid.uuid4()),
        "email": body.email,
        "password": body.password,
        "fullname": body.fullname,
        "photo": body.photo,
    }
    result = await createUser(db, data)

    # Response
    if result.get("success") == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return {
        "message": "Insert success",
        "data": body
    }

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update(
    id,
    body: Body,
    response: Response,
    db: Session = Depends(get_db)
):

    # Validate id
    data = await getUserById(db, id)
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": "Data is not found"
        }

    # Validate existing email
    user = await getUserByEmail(db, body.email, id)
    if user is None:
        user = await getUserByEmail(db, body.email)
        if user is not None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "message": "Email is already taken, please try another one"
            }

    # Preparing to update
    data.email = body.email
    data.fullname = body.fullname
    
    # Check for password hash
    if body.password != "" and body.password is not None:
        encoded_password = body.password.encode("utf-8")
        data.password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode("utf-8")

    # Update data
    result = await updateUser(db, data)

    # Response
    if result.get("success") == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return {
        "message": "Update success",
        "data": body
    }

@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
async def remove(
    id,
    response: Response,
    db: Session = Depends(get_db)
):
    # Validate id
    data = await getUserById(db, id)
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "message": "Data is not found" }

    # Update data
    data.deleted = True
    result = await updateUser(db, data)

    # Response
    if result.get("success") == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return {
        "message": "Delete success",
        "id": id
    }
