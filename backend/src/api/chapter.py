from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .. import models
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=models.ChapterInDB)
async def create_chapter(chapter: models.ChapterCreate, db: Session = Depends(get_db)):
    db_chapter = models.Chapter(**chapter.model_dump())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

@router.get("/", response_model=List[models.ChapterInDB])
async def read_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chapters = db.query(models.Chapter).offset(skip).limit(limit).all()
    return chapters

@router.get("/{chapter_id}", response_model=models.ChapterInDB)
async def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return db_chapter

@router.put("/{chapter_id}", response_model=models.ChapterInDB)
async def update_chapter(chapter_id: int, chapter: models.ChapterCreate, db: Session = Depends(get_db)):
    db_chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    for key, value in chapter.model_dump().items():
        setattr(db_chapter, key, value)

    db.commit()
    db.refresh(db_chapter)
    return db_chapter

@router.delete("/{chapter_id}", response_model=models.ChapterInDB)
async def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    db.delete(db_chapter)
    db.commit()
    return db_chapter
