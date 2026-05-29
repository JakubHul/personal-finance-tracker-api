from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.database.models import TransactionDB

def calculate_stats(db: Session, user_id: int, month: str | None = None):
    query = db.query(TransactionDB).filter(TransactionDB.user_id == user_id)

    if month:
        year, mon = month.split("-")
        query = query.filter(
            extract("year", TransactionDB.date) == int(year),
            extract("month", TransactionDB.date) == int(mon),
        )

    transactions = query.all()

    total_expenses = 0
    total_number = len(transactions)
    max_amount = 0

    for t in transactions:
        if max_amount < t.amount:
            max_amount = t.amount

    for t in transactions:
        total_expenses += t.amount

    return {
        "total_expenses": total_expenses,
        "total_number": total_number,
        "max_amount": max_amount,
    }