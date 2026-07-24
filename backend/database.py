import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for local dev — zero setup. Swap this for a Postgres URL when you deploy,
# e.g. "postgresql://user:pass@host:5432/dbname"
# DATABASE_URL = "sqlite:///./shortener.db"

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./shortener.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Using DATABASE_URL starting with: {DATABASE_URL[:15]}")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
