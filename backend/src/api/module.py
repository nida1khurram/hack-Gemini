from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .. import models
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=models.ModuleInDB)
async def create_module(module: models.ModuleCreate, db: Session = Depends(get_db)):
    db_module = models.Module(**module.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/", response_model=List[models.ModuleInDB])
async def read_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    modules = db.query(models.Module).offset(skip).limit(limit).all()
    return modules

@router.get("/{module_id}", response_model=models.ModuleInDB)
async def read_module(module_id: int, db: Session = Depends(get_db)):
    db_module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.put("/{module_id}", response_model=models.ModuleInDB)
async def update_module(module_id: int, module: models.ModuleCreate, db: Session = Depends(get_db)):
    db_module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    for key, value in module.model_dump().items():
        setattr(db_module, key, value)

    db.commit()
    db.refresh(db_module)
    return db_module

@router.delete("/{module_id}", response_model=models.ModuleInDB)
async def delete_module(module_id: int, db: Session = Depends(get_db)):
    db_module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    db.delete(db_module)
    db.commit()
    return db_module
