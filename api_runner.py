import time
from utilities.database import init_db_storage, close_db_storage
from utilities.config import get_settings
from api.infor import router as infor_router
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # replacement of @app.on_event("startup")
    print("ASYNC startup: Initializing resources...")
    await init_db_storage()
    yield
    # replacement of @app.on_event("shutdown")
    print("ASYNC shutdown: Releasing resources...")
    await close_db_storage()

app = FastAPI(lifespan=lifespan)
app.include_router(infor_router)

# CORS
origins = [
    "http://localhost:8001",  # Your frontend URL
    "https://yourdomain.com", # Your production frontend URL
    # Add other allowed origins as needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Customized middelware
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration )
    return response

# Static files access
settings = get_settings()
Path(settings.static_storage_path).mkdir(parents=True, exist_ok=True)
app.mount("/static_files", StaticFiles(directory=settings.static_storage_path), name="static_files")
