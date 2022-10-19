import enum
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
        title: str
        content: str
        published: bool = True
        rating: Optional[int] = None


my_posts = [{"title":"Title1", "content":"content1", "id":1},
            {"title":"Title2", "content":"content2", "id":2},
            {"title":"Title3", "content":"content3", "id":3}]

def find_post(id):
        for p in my_posts:
                if p["id"]==id:
                        return p
def find_post_index(id):
        for i, p in enumerate(my_posts):
                if p['id'] == id:
                        return i

@app.get("/")
async def root():
        return{"message":"Hello world!!"}

@app.get("/posts")
async def get_posts():
        return{"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
        post_dict = post.dict()
        post_dict['id'] = randrange(0,100000)
        my_posts.append(post_dict)
        return{"data":post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
        post = find_post(id)
        if not post:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail=f"post with id: {id} was not found")
        return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
        index = find_post_index(id)
        if index == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail=f"post with id: {id} was not found")
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
        index = find_post_index(id)
        if index == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail=f"post with id: {id} was not found")
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {'data': post_dict}