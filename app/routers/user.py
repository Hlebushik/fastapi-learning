from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user.email}' already exists."
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id '{id}' not found."
    )