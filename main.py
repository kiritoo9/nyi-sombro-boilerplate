import uvicorn
from fastapi import FastAPI, status, Request, Depends
from fastapi.responses import JSONResponse
from src.configs.config import settings
from src.configs.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from src.configs.database import Base, engine

# Import routes
import src.routes.auth as auth_routes
import src.routes.user as user_routes

# Config application
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    create_tables()
    return app

app = start_application()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

# welcome route
@app.get("/")
async def welcome():
    return {
        "greeting": f'Welcome to our {settings.APP_NAME}',
        "version": f'{settings.APP_VERSION}'
    }

# Regist transactional routes
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

# Run
def main() -> None:
    uvicorn.run("main:app", host=settings.APP_HOST, port=int(settings.APP_PORT))

if __name__ == "__main__":
    main()