from src.configs.config import settings
from typing import Union
from fastapi import FastAPI
import src.routes.user as user

def create_tables():
    pass

def start_application():
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    create_tables()
    return app

app = start_application()

# initiate routes
app.include_router(user.router)

@app.get("/")
async def welcome():
    return {
        "greeting": f'Welcome to our {settings.APP_NAME}',
        "version": f'{settings.APP_VERSION}'
    }