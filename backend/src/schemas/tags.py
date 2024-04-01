from pydantic import BaseModel


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

