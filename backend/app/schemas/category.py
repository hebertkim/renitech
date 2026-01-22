from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, Dict, Any
from uuid import UUID
import json

# -------------------------
# BASE
# -------------------------
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    type: Literal["income", "expense", "transfer"]
    parent_id: Optional[UUID] = None
    description: Optional[str] = None
    fiscal_class: Optional[str] = None
    ai_rules: Optional[Dict[str, Any]] = None

    @validator("ai_rules", pre=True)
    def parse_ai_rules(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("ai_rules must be a valid JSON string or dict")
        return v

# -------------------------
# CREATE
# -------------------------
class CategoryCreate(CategoryBase):
    pass

# -------------------------
# UPDATE
# -------------------------
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    type: Optional[Literal["income", "expense", "transfer"]] = None
    parent_id: Optional[UUID] = None
    description: Optional[str] = None
    fiscal_class: Optional[str] = None
    ai_rules: Optional[Dict[str, Any]] = None

    @validator("ai_rules", pre=True)
    def parse_ai_rules(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("ai_rules must be a valid JSON string or dict")
        return v

# -------------------------
# OUTPUT / RESPONSE
# -------------------------
class CategoryOut(CategoryBase):
    id: UUID

    class Config:
        from_attributes = True

# -------------------------
# DELETE RESPONSE
# -------------------------
class CategoryDeleteOut(BaseModel):
    detail: str
