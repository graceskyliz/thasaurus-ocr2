import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://JQTfOoXUrCuzJwAtONMazjNZlgqgUKnz@switchyard.proxy.rlwy.net:38303/railway",
)

# SQLAlchemy engine and session (synchronous)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
