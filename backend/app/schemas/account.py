from pydantic import BaseModel, Field

class AccountBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    balance: float = 0.0

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    class Config:
        from_attributes = True
