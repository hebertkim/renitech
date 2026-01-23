from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import ProductCategorySchema
from app import crud
from app.database import get_db
from uuid import UUID
from typing import List

router = APIRouter()

@router.post("/categories/", response_model=ProductCategorySchema)
def create_category(category: ProductCategorySchema, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category_data=category)

@router.get("/categories/{category_id}", response_model=ProductCategorySchema)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/categories/", response_model=List[ProductCategorySchema])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db=db, skip=skip, limit=limit)
