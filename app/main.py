from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, User, Expense



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str

@app.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not existing_user:
        return {
            "error": "User not found"
        }

    if existing_user.password != user.password:
        return {
            "error": "Invalid password"
        }

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "username": existing_user.username,
        "email": existing_user.email
    }


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API"
    }


@app.get("/app")
def frontend(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        return {
            "error": "Email already registered"
        }

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

@app.post("/expenses")
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {
        "message": "Expense added successfully",
        "expense_id": new_expense.id,
        "title": new_expense.title,
        "amount": new_expense.amount,
        "category": new_expense.category
    }

@app.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).all()

    return expenses

@app.get("/expenses/total")
def get_total_expenses(
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).all()

    total = sum(
        expense.amount
        for expense in expenses
    )

    return {
        "total_expenses": round(total, 2),
        "number_of_expenses": len(expenses)
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        for user in users
    ]


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

    if not expense:
        return {
            "error": "Expense not found"
        }

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }