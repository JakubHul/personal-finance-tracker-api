from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user
from app.schemas import Budget, BudgetDataOut, BudgetDeletedOut, BudgetOut
from app.database.database import get_db
from app.database.models import BudgetDB

router = APIRouter()


@router.get("/budgets", response_model=list[BudgetOut])
def get_budgets(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return db.query(BudgetDB).filter(BudgetDB.user_id == user_id).all()


@router.get("/budgets/{budget_id}", response_model=BudgetOut)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    budget = db.query(BudgetDB).filter(
        BudgetDB.id == budget_id,
        BudgetDB.user_id == user_id,
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    return budget


@router.post("/budgets", response_model=BudgetDataOut, status_code=201)
def create_budget(
    budget: Budget,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    db_budget = BudgetDB(
        name=budget.name,
        limit=budget.limit,
        user_id=user_id,
    )

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    return {
        "message": "Budget created",
        "data": db_budget,
    }


@router.delete("/budgets/{budget_id}", response_model=BudgetDeletedOut)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    budget = db.query(BudgetDB).filter(
        BudgetDB.id == budget_id,
        BudgetDB.user_id == user_id,
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()

    return {
        "message": "Budget deleted",
        "deleted": budget,
    }


@router.put("/budgets/{budget_id}", response_model=BudgetDataOut)
def update_budget(
    budget_id: int,
    budget: Budget,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    db_budget = db.query(BudgetDB).filter(
        BudgetDB.id == budget_id,
        BudgetDB.user_id == user_id,
    ).first()

    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db_budget.name = budget.name
    db_budget.limit = budget.limit

    db.commit()
    db.refresh(db_budget)

    return {
        "message": "Budget updated",
        "data": db_budget,
    }
