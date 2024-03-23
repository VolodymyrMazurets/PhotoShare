# File to export the API routes. Below is example how to use

# from fastapi import APIRouter

# from src.api.routes import login

# api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])

# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models
from ..core.db import get_db, engine
from ..schemas import TagList

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/images/{image_id}/tags/", response_model=TagList)
async def add_tags(image_id: int, tags: TagList, db: Session = Depends(get_db)):
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

