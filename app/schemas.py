from pydantic import BaseModel,Field

class BookCreate(BaseModel):
    title: str = Field(min_length = 1, max_length=100)
    author : str = Field(min_length = 1, max_length=100)
    description :str | None = None
    price : int = Field(gt=0)  # Price must be greater than 0

class BookResponse(BaseModel):
    id: int
    title: str
    author : str
    description :str | None = None
    price : int

    class Config:
        from_attributes = True
