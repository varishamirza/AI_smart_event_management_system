try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base
    from sqlalchemy.orm import Session
    from typing import Generator
except Exception as e:
    raise ImportError(f"Failed to import database dependencies: {e}")

SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"

# create engine and session factory
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Explicit exports (helps `from app.database import ...`)
__all__ = ["engine", "SessionLocal", "Base", "get_db"]