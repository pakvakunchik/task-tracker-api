from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.constants import SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)
Session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()




