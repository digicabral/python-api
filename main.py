from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
        title: str
        content: str
        published: bool = True
        rating: Optional[int] = None

@app.get("/")
async def root():
        return{"message":"Hello world!!"}

@app.get("/posts")
async def get_posts():
        return{"data":"posts"}

@app.post("/createposts")
async def create_posts(new_post: Post):
        print(new_post)
        return{"message":"newpost"}