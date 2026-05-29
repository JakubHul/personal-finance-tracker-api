from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user
from app.database.database import get_db
from app.routes.auth import router as auth_router
from app.routes.budgets import router as budget_router
from app.routes.transactions import router as transaction_router
from app.schemas import StatsOut
from app.services.stats import calculate_stats

app = FastAPI()


@app.get("/")
@app.head("/")
def root():
    return {"message": "API is working"}


@app.get("/stats", response_model=StatsOut)
def get_stats(
    month: str | None = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    if month:
        parts = month.split("-")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise HTTPException(status_code=400, detail="month must be in YYYY-MM format")
    return calculate_stats(db=db, user_id=user_id, month=month)


app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(auth_router)