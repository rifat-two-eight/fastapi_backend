from fastapi import FastAPI,HTTPException,status,Response,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from sqlalchemy.orm import Session
from .database import get_db,engine
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# database Postgresql
while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'postgres',user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('successfully connected database')
        break
    except Exception as error:
        print("failed connected database")
        print("Error",error)
        time.sleep(2)


# alchemy
@app.get("/coursealchemy",response_model=List[schemas.CourseResponse])
def course(db:Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

@app.get("/coursealchemy/{id}",response_model=schemas.CourseResponse)
def get_single(id:int,db:Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"course with id {id} not found"
        )
    return course

@app.post("/coursealchemy",response_model=schemas.CourseResponse)
def create_course(course:schemas.CourseCreate,db:Session = Depends(get_db)):
    new_course = models.Course(
    name=course.name,
    instructor=course.instructor,
    duration=course.duration,
    website=str(course.website)
)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.put("/coursealchemy/{id}",response_model=schemas.CourseResponse)
def update_single(id: int,updated_course: schemas.CourseCreate,db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with id {id} not found"
        )

    update_data = updated_course.model_dump()
    update_data["website"] = str(update_data["website"])

    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@app.delete("/coursealchemy/{id}")
def delete_course(id:int,db:Session=Depends(get_db)):
    course_query=db.query(models.Course).filter(models.Course.id==id)
    course=course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"course with id {id} not exists")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# user table
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserRes)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(400,"Email already exists")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user