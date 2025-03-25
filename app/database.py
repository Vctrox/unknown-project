# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
import time

# Configure MariaDB connection
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "user_management")

# Construct SQLAlchemy database URL for MariaDB
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_engine(retry_count=3, delay=5):
    """
    Create SQLAlchemy engine with retry mechanism
    """
    for attempt in range(retry_count):
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
                # Add connection testing
                pool_pre_ping=True
            )
            # Test connection
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return engine
        except SQLAlchemyError as e:
            if attempt < retry_count - 1:
                print(f"Database connection failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e

# Create engine with retry mechanism
engine = get_engine()

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)