import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Change asyncpg -> psycopg2 in your DATABASE_URL env var, or override here:
# DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# scoped_session isolates sessions per thread — safe for Flask's threaded model
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return SessionLocal()