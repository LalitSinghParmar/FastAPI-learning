from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from sqlalchemy import TIMESTAMP


class Vote(BaseModel):
    post_id : int
    vote_dir : conint(le=1)

class User(BaseModel):
    email : EmailStr
    password : str

class getUser(BaseModel):
    email : EmailStr
    id : str
    created_at : datetime

    class Config:
        orm_mode = True

class BasePost(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(BasePost):
    pass

class Post(BasePost):
    id : int
    create_at : datetime
    owner : getUser

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str]=None



