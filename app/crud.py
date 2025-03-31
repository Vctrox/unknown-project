# app/crud.py

# import
from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, user_id: int):
    """
    Retrieve a user by ID
    """
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve multiple users with pagination
    """
    return db.query(models.UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: models.UserCreate):
    """
    Create a new user
    """
    db_user = models.UserModel(
        username=user.username, 
        email=user.email, 
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: models.UserUpdate):
    """
    Update an existing user
    """
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    if user_update.email:
        db_user.email = user_update.email
    if user_update.full_name:
        db_user.full_name = user_update.full_name
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Delete a user
    """
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user