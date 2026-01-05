from pydantic import BaseModel, Field


class Movie(BaseModel):
    title: str
    year: int
    genre: str
    rating: int = Field(
        gt=0, 
        lt=11, 
        description="Rating must be between 1 and 10, the higher the better")
    
    
class Prompt(BaseModel):
    prompt: str