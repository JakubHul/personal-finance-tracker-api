from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user
from app.database.database import get_db
from app.database.models import TransactionDB
from app.schemas import Transaction, TransactionDataOut, TransactionDeletedOut, TransactionOut

router = APIRouter()


@router.get("/transactions", response_model=list[TransactionOut])
def get_transactions(
    category: str | None = None,
    min_amount: float | None = None,
    month: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    query = db.query(TransactionDB).filter(TransactionDB.user_id == user_id)

    if category:
        query = query.filter(TransactionDB.category == category)

    if min_amount is not None:
        query = query.filter(TransactionDB.amount >= min_amount)

    if month:
        try:
            month_date = datetime.strptime(month, "%Y-%m")
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="month must be in YYYY-MM format") from exc

        query = query.filter(
            extract("year", TransactionDB.date) == month_date.year,
            extract("month", TransactionDB.date) == month_date.month,
        )

    if date_from is not None:
        date_from_dt = datetime.combine(date_from, datetime.min.time())
        query = query.filter(TransactionDB.date >= date_from_dt)

    if date_to is not None:
        date_to_dt = datetime.combine(date_to + timedelta(days=1), datetime.min.time())
        query = query.filter(TransactionDB.date < date_to_dt)

    if sort not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="sort must be 'asc' or 'desc'")

    if sort == "desc":
        query = query.order_by(TransactionDB.date.desc())
    else:
        query = query.order_by(TransactionDB.date.asc())

    data = query.all()

    return data

@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    transaction = db.query(TransactionDB).filter(
        TransactionDB.id == transaction_id,
        TransactionDB.user_id == user_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.post("/transactions", response_model=TransactionOut, status_code=201)
def add_transaction(
    transaction: Transaction,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    payload = {
        "amount": transaction.amount,
        "category": transaction.category,
        "user_id": user_id,
    }
    if transaction.date is not None:
        payload["date"] = transaction.date

    db_transaction = TransactionDB(**payload)

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

@router.delete("/transactions/{transaction_id}", response_model=TransactionDeletedOut)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    transaction = db.query(TransactionDB).filter(
        TransactionDB.id == transaction_id,
        TransactionDB.user_id == user_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted",
        "deleted": transaction
    }

@router.put("/transactions/{transaction_id}", response_model=TransactionDataOut)
def update_transaction(
    transaction_id: int,
    transaction: Transaction,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    db_transaction = db.query(TransactionDB).filter(
        TransactionDB.id == transaction_id,
        TransactionDB.user_id == user_id
    ).first()

    if not db_transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db_transaction.amount = transaction.amount
    db_transaction.category = transaction.category

    db.commit()
    db.refresh(db_transaction)

    return {
        "message": "Transaction updated",
        "data": db_transaction
    }