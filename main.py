from typing import Optional
from fastapi import  FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange




app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating : Optional[int]=None


mypost = [{"title": "title of post 1", "content": "content of post 1", "id": 1 }, {"title": "favorite food", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in mypost:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Welcome to my api!!!"}

@app.get("/posts")
def get_post():
    return {"data": mypost}

@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    mypost.append(post_dict)
    
    return {"data": post} 


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_details": f"Here is post {post}"}
    
