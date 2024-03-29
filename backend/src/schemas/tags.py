from pydantic import BaseModel
from typing import List


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

