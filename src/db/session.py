from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

engine = create_engine(settings.db_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)
