from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Course(BaseModel):
    name: str
    district: str
    number: float
    is_top: bool
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
    return {"data":post}


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
