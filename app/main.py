import logging
from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.json_logging_middleware import LoggingMiddleware
from app.employees.router import router as employee_router
from app.auth.router import router as auth_router
from app.core.logger import setup_logger

app = FastAPI()
setup_logger()

Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
logger.info("logger is added")
app.add_middleware(LoggingMiddleware)

app.include_router(employee_router)
app.include_router(auth_router)
