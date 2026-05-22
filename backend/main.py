from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.init_scan import scan_repo
from routes.index import router as routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    files = scan_repo()
    app.state.files = files  # store for later
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
