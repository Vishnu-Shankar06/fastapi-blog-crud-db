from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=7)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str|None = Field(min_length=3)
    content: str|None = Field(min_length=7)

class PostResponse(PostBase):
    id: int