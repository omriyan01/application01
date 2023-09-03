from fastapi import FastAPI
# from fastapi.params import Body
# from typing import Optional, List
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
# from sqlalchemy.orm import Session
from .routers import post, user, auth
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def get_index():
    html_file_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_file_path)


@app.post("/process_data")
async def process_data(data: dict):
    processed_data = {"message": f"Received data: {data}"}
    return processed_data

while True:

    try:
        conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password='Hapoel69', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull ")
        break
    except Exception as error:
        print("connection failed")
        print("Error", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "welcome to my web"} 


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]
