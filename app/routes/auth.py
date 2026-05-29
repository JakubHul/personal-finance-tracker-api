from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import UserDB
from app.schemas import LoginRequest, MeOut, RegisterResponse, TokenOut, User, UserOut
from app.auth.security import hash_password
from app.auth.security import verify_password
from app.auth.auth import create_access_token
from app.auth.auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(user: User, db: Session = Depends(get_db)):

    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserDB(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "id": new_user.id,
        "email": new_user.email
    }

@router.post("/login", response_model=TokenOut)
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(db_user.id),
        "email": db_user.email,
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=MeOut)
def me(user_id: int = Depends(get_current_user)):
    return {
        "user_id": user_id
    }