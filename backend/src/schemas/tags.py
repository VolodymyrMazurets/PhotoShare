from pydantic import BaseModel
from typing import List


class TagList(BaseModel):
    tags: List[str]
