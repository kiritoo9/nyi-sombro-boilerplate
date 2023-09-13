import math
from fastapi import APIRouter, Response, status, Path, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.configs.database import get_db
from src.businesses.user import getUserLists, getUserCount, getUserById

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
async def create(body: BodyInsert):
    return {
        "message": "Data inserted",
        "body": body
    }

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update(body: Body):
    return {
        "message": "Data updated",
        "body": body
    }