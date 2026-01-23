# app/routes/product.py
from app import crud, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.database import get_db

router = APIRouter()

# Obter todos os produtos
@router.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)

# Obter um produto específico
@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    return crud.get_product(db=db, product_id=product_id)

# Criar um novo produto
@router.post("/products/", response_model=schemas.Product)
def create_product(product_data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product_data=product_data)

# Atualizar um produto
@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: str, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    return crud.update_product(db=db, product_id=product_id, product=product)

# Excluir um produto
@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id)

# Criar SKU para um produto (caso queira tratar o SKU de forma independente)
# **Agora este endpoint não é mais necessário, pois o SKU já faz parte do modelo Product**
# @router.post("/products/{product_id}/sku", response_model=schemas.Product)
# def create_sku_for_product(
#     product_id: str, sku_data: schemas.SKUCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_sku(db=db, product_id=product_id, sku_data=sku_data)

# Obter SKU de um produto (caso esteja tratando isso separadamente)
# **Não é mais necessário, pois o SKU agora é parte do modelo Product**
# @router.get("/products/{product_id}/sku", response_model=schemas.SKU)
# def get_skus_of_product(product_id: str, db: Session = Depends(get_db)):
#     return crud.get_skus_by_product_id(db=db, product_id=product_id)
