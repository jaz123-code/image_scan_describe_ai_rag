from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

engine=create_engine("sqlite:///./image.db")
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
