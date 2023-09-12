from fastapi import FastAPI, status
from src.configs.config import settings
from pydantic import BaseModel
from typing import Union
import src.routes.user as user
import uvicorn

def create_tables():
    pass

def start_application():
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    create_tables()
    return app

app = start_application()

# Health Check
class HealthCheck(BaseModel):
    status: str = "OK"

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

# initiate routes
app.include_router(user.router)

@app.get("/")
async def welcome():
    return {
        "greeting": f'Welcome to our {settings.APP_NAME}',
        "version": f'{settings.APP_VERSION}'
    }

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=3000)

if __name__ == "__main__":
    main()