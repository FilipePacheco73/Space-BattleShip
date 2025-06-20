# app/routes/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database import create_schemas as models
from backend.app.database import create_database as database_config
from backend.app import schemas
from backend.app.crud import ship_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_db(): # This get_db can be DRYed up later by moving to a common utility
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserResponse)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return ship_crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.UserResponse])
def list_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = ship_crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = ship_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user