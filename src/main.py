from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.adapters.auth import get_auth
from src.adapters.database import Base, engine
from src.api.routes import customers_router
from src.config import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


api = FastAPI(
    title="Order Service API",
    debug=settings.DEBUG,
    description="you know, for orders",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": settings.OPENID_CONNECT_CLIENT_ID,
        "scopes": ["openid", "profile", "email", "phone"],
        "pkceMethod": "S256",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Development environment"},
    ],
    root_path_in_servers=False,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/", include_in_schema=False, tags=["ping"])
def pong():
    return {
        "message": "Welcome to the Order Service API. Visit /docs for documentation."
    }


api.include_router(
    customers_router, dependencies=[Depends(get_auth)], tags=["customers"]
)
