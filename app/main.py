from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, users, capabilities, audit
from app.config import settings
from app.database import init_db

app = FastAPI(
    title="TRUSTCORE AAIRA",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(capabilities.router, prefix="/api/v1")
app.include_router(audit.router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["system"])
async def root():
    return {"message": "TRUSTCORE AAIRA API"}


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}
