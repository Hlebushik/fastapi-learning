from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class PostResponse(PostBase):
    id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True

class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore

    class Config:
        from_attributes = True