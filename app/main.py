import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.auth.router import router as auth_router
from app.core.database import Base, engine
from app.core.json_logging_middleware import LoggingMiddleware
from app.core.logger import setup_logger
from app.employees.router import router as employee_router

app = FastAPI()
setup_logger()

Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
logger.info("logger is added")
app.add_middleware(LoggingMiddleware)


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(employee_router)
app.include_router(auth_router)
