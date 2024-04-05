from sqlalchemy.orm import Session
from src.models.base import Tag

def create_tag_if_not_exist(tag_name: str, db: Session):
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    return tag
