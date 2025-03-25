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

def create_database_if_not_exists(engine):
    """
    Create database if it doesn't exist
    """
    try:
        with engine.connect() as conn:
            conn.execute("commit")
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except Exception as e:
        print(f"Error creating database: {e}")

def get_engine(retry_count=5, delay=5):
    """
    Create SQLAlchemy engine with robust retry mechanism
    """
    for attempt in range(retry_count):
        try:
            # Create an initial connection to the MySQL server
            initial_engine = create_engine(
                f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/mysql",
                pool_pre_ping=True
            )
            
            # Attempt to create database if not exists
            create_database_if_not_exists(initial_engine)
            
            # Create the final engine with the specific database
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True
            )
            
            # Test connection
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            
            return engine
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < retry_count - 1:
                time.sleep(delay)
            else:
                raise

# Create engine with retry mechanism
engine = get_engine()

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)