# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr, constr

Base = declarative_base()

class UserModel(Base):
    """
    SQLAlchemy database model for users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Specify length for VARCHAR
    email = Column(String(100), unique=True, index=True)     # Specify length for VARCHAR
    full_name = Column(String(100)) 

class UserCreate(BaseModel):
    """
    Pydantic model for user creation
    """
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: str

class UserUpdate(BaseModel):
    """
    Pydantic model for user updates
    """
    email: EmailStr = None
    full_name: str = None

class User(BaseModel):
    """
    Pydantic model for user response
    """
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        from_attributes  = True