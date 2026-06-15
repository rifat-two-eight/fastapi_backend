from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db,engine
from .. import models,schemas

router = APIRouter(
    prefix="/course"
)

# alchemy
@router.get("/",response_model=List[schemas.CourseResponse])
def course(db:Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

@router.get("/{id}",response_model=schemas.CourseResponse)
def get_single(id:int,db:Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"course with id {id} not found"
        )
    return course

@router.post("/",response_model=schemas.CourseResponse)
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

@router.put("/{id}",response_model=schemas.CourseResponse)
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

@router.delete("/{id}")
def delete_course(id:int,db:Session=Depends(get_db)):
    course_query=db.query(models.Course).filter(models.Course.id==id)
    course=course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"course with id {id} not exists")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)