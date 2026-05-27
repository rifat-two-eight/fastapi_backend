from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"name":"rifat"}

@app.get("/details")
def view_details():
    return {"phone":"iphone","brand":"oppo","price": 15000}