import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from src.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.core.config import settings
from pathlib import Path
from fastapi_limiter import FastAPILimiter

BASE_DIR = Path(__file__).resolve().parent

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.REDIS_HOST_, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"FRONTEND_URL": settings.FRONTEND_URL, "BACKEND_URL": settings.BACKEND_URL, "ADMINER_URL": settings.ADMINER_URL})
