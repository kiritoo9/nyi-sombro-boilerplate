from fastapi import APIRouter, Response, status, Path
from pydantic import BaseModel, Field

# Request body model
class Body(BaseModel):
    email: str | None = Field(
        title="Email cannot be empty", max_length=50, min_length=5
    )
    password: str | None = Field(
        default=None, min_length=6
    )
    fullname: str | None = Field(
        title="Fullname cannot be empty", min_length=1
    )
    photo: str | None = None

class BodyInsert(Body):
    password: str | None = Field(
        title="Password cannot be empty", min_length=6
    )

# Set up Route
router = APIRouter(
    prefix = "/user",
    tags = ["master.user"]
)

@router.get("/", status_code=200) # set default response code
async def list():
    return {
        "greeting": "This is user listing"
    }

@router.get("/{id}", status_code=200)
async def detail(id, response: Response):
    data = None
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND # Custom response status
        return {
            "message": "Data is not found"
        }

    return {
        "message": "This is detail",
        "id": id
    }

@router.post("/", status_code=201)
async def create(
    body: BodyInsert
):
    return {
        "message": "Data inserted",
        "body": body
    }

@router.put("/{id}", status_code=201)
async def update(body: Body):
    return {
        "message": "Data updated",
        "body": body
    }