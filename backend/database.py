from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for local dev — zero setup. Swap this for a Postgres URL when you deploy,
# e.g. "postgresql://user:pass@host:5432/dbname"
DATABASE_URL = "sqlite:///./shortener.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
