from fastapi import HTTPException
from sqlalchemy.orm import Session
from src import models
from src.core.db import SessionLocal
from src.schemas import TagList

def add_tags_func(image_id: int, tags: TagList):
    if len(tags.tags) > 5:
        raise HTTPException(status_code=400, detail="Cannot add more than 5 tags")

    db = SessionLocal()
    try:
        image = db.query(models.Image).filter(models.Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        added_tags = []
        for tag_name in tags.tags:
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.add(tag)
                try:
                    db.commit()
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=500, detail="Could not create tag")
                db.refresh(tag)
            added_tags.append(tag.name)

        return {"tags": added_tags}
    finally:
        db.close()
