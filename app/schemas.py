from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- request schemas ----------

class Transaction(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    date: datetime | None = None


class Budget(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    limit: float = Field(gt=0)


class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- response schemas ----------

class TransactionOut(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime | None
    created_at: datetime | None
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class BudgetOut(BaseModel):
    id: int
    name: str
    limit: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    email: str


class RegisterResponse(BaseModel):
    message: str
    id: int
    email: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class MeOut(BaseModel):
    user_id: int


class StatsOut(BaseModel):
    total_expenses: float
    total_number: int
    max_amount: float


# --- wrappers for mutating responses ---

class TransactionDataOut(BaseModel):
    message: str
    data: TransactionOut

    model_config = ConfigDict(from_attributes=True)


class TransactionDeletedOut(BaseModel):
    message: str
    deleted: TransactionOut

    model_config = ConfigDict(from_attributes=True)


class BudgetDataOut(BaseModel):
    message: str
    data: BudgetOut

    model_config = ConfigDict(from_attributes=True)


class BudgetDeletedOut(BaseModel):
    message: str
    deleted: BudgetOut

    model_config = ConfigDict(from_attributes=True)
