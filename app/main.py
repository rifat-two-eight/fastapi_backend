from fastapi import FastAPI,HTTPException,status,Response,Depends
from pydantic import BaseModel,HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import get_db,engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

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


@app.get("/")
def root():
    cursor.execute(""" SELECT * FROM course """)
    data= cursor.fetchall()
    return {"data":data}

@app.post("/course")
def create_post(post:Course):
    cursor.execute("""insert into course(name,instructor,duration,website) values(%s,%s,%s,%s) returning *""",(post.name,post.instructor,post.duration,str(post.website)) )
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}


@app.get("/details")
def view_details():
    return {"phone":"iphone","brand":"oppo","price": 15000}

@app.get("/teams")
def world_cup():
    return {"champion":"Argentina","year":"2022"}

@app.get("/name")
def show_name():
    return {"person1":"rifat","person2":"laiju","person3":"ambia","person4":"mizan"}

@app.get("/age")
def show_age():
    return {"karim":28,"rahim":35}

@app.get("/course/{id}")
def show_details(id:int):
    cursor.execute("""select * from course where id=%s""",(str(id),))
    details = cursor.fetchone()
    if not details:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"course with id {id} not found"
        )
    return {"course details":details}

@app.delete("/course/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_course(id:int):
    cursor.execute("""delete from course where id=%s returning *""",(str(id),))
    deleted_course = cursor.fetchone()
    conn.commit()
    if deleted_course==None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail = f"course with id {id} not exist")
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.put("/course/{id}")
def update_course(id:int,course:Course):
    cursor.execute("""update course set name=%s,instructor=%s,duration=%s,website=%s where id=%s returning * """,(course.name,course.instructor,course.duration,str(course.website),str(id)))
    updated_course= cursor.fetchone()
    conn.commit()

    if updated_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"course with id {id} does not exist")
    return{"data":updated_course}

# alchemy
@app.get("/coursealchemy")
def course(db:Session = Depends(get_db)):
    course = db.query(models.Course).all()
    return {"course":course}

@app.get("/coursealchemy/{id}")
def get_single(id:int,db:Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"course with id {id} not found"
        )
    return {"course details": course}

@app.post("/coursealchemy")
def create_course(course:Course,db:Session = Depends(get_db)):
    new_course = models.Course (
        name = course.name,
        instructor = course.instructor,
        duration = course.duration,
        website = str(course.website)
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"course":new_course}

@app.put("/coursealchemy/{id}")
def update_single(id: int,updated_course: Course,db: Session = Depends(get_db)):
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
    return {"course details": course}

@app.delete("/coursealchemy/{id}")
def delete_course(id:int,db:Session=Depends(get_db)):
    course_query=db.query(models.Course).filter(models.Course.id==id)
    course=course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"course with id {id} not exists")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)