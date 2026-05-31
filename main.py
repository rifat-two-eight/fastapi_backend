from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl

app = FastAPI()

class Course(BaseModel):
    name: str
    district: str
    number: float
    is_top: bool
    website: HttpUrl

# database

@app.post("/course")
def create_post(post:Course):
    return {"data":post}

@app.get("/")
def root():
    return {"name":"rifat"}

@app.get("/details")
def view_details():
    return {"phone":"iphone","brand":"oppo","price": 15000}

@app.get("/teams")
def world_cup():
    return {"champion":"Argentina","year":"2022"}

@app.get("/name")
def show_name():
    return {"person1":"rifat","person2":"laiju","person3":"ambia","person4":"mizan"}
