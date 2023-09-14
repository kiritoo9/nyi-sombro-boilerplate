import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from src.configs.config import settings
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.configs.database import Base, engine
from src.middlewares.verify import verifyToken

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

# Middleware
@app.middleware("http")
async def __verifyToken(request: Request, call_next):
    requested_url = None

    # Get url request
    url = str(request.url)
    url = url.split(f':{settings.APP_PORT}')
    if len(url) > 1:
        url = url[1].split("?")
        if len(url) > 0:
            requested_url = url[0]

            # Remove slash in last character
            last = requested_url[len(requested_url)-1:]
            if last == "/":
                requested_url = requested_url[0:len(requested_url)-1]

    # Free pass middleware check by route
    free_pass_routes = [
        "","/auth/login"
    ]
    if requested_url is not None:
        if requested_url not in free_pass_routes:
            middleware_response = await verifyToken(request.headers.get("Authorization"))
            if middleware_response.get("code") == 401:
                return JSONResponse(status_code=middleware_response.get("code"), content={ "message": middleware_response.get("message")} )

    response = await call_next(request)
    return response

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
        "greeting": f'Welcome to {settings.APP_NAME}',
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