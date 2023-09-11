from fastapi import APIRouter, Response, status

router = APIRouter(
    prefix = "/user",
    tags = ["master.user"]
)

@router.get("/", status_code=200) # set default response code
async def list(response: Response):
    response.status_code = status.HTTP_201_CREATED # Custom response status

    return {
        "greeting": "This is user listing"
    }