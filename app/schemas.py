from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime



class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  

class PostOut(BaseModel):
    Post: Post  # Nested Post model
    votes: int  # Vote count

    class Config:
        from_attributes = True
    

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
