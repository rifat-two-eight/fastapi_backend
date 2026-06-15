from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users"
)


# user table
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data = user.model_dump()

    user_data["password"] = utils.hash_password(user.password)

    new_user = models.User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user