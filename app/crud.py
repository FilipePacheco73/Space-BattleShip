# app/crud.py
from sqlalchemy.orm import Session
from app.database import create_schemas as models
from app import schemas

# --- Ship CRUD Operations ---
def get_ship(db: Session, ship_id: int):
    return db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()

def get_ships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ship).offset(skip).limit(limit).all()

def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = models.Ship(**ship.dict())
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

def update_ship(db: Session, ship_id: int, ship_data: schemas.ShipCreate):
    db_ship = db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()
    if db_ship:
        for key, value in ship_data.dict(exclude_unset=True).items():
            setattr(db_ship, key, value)
        db.commit()
        db.refresh(db_ship)
    return db_ship

def delete_ship(db: Session, ship_id: int):
    db_ship = db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()
    if db_ship:
        db.delete(db_ship)
        db.commit()
        return True
    return False

# --- User CRUD Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Add update_user and delete_user if you want them, following the ship pattern
# For now, only create_user, get_user, get_users are implemented as per existing user routes.
