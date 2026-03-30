from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from constants import SQLALCHEMY_DATABASE_URI

Base = DeclarativeBase()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_local = sessionmaker(bind=engine)
