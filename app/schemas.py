from pydantic import BaseModel,HttpUrl

class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    id : int

    class Config:
        orm_model = True
