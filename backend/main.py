from contextlib import asynccontextmanager
import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.init_scan import scan_repo
from services.watcher import start_watcher  # ADD
from routes.index import router as routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    files = scan_repo()
    app.state.files = files

    loop = asyncio.get_event_loop()  # ADD
    observer = start_watcher(os.environ["REPO_PATH"], loop)  # ADD

    yield

    observer.stop()  # ADD
    observer.join()  # ADD


app = FastAPI(lifespan=lifespan)
app.include_router(routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
