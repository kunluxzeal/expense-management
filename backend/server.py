from fastapi import  FastAPI , HTTPException
from datetime import date
import db_helpers
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()


origins = [
    "https://your-frontend-url.onrender.com",  # Streamlit app URL
    "http://localhost",  # optional for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/expenses/{expense_date}" ,response_model =List[Expense])
async def get_expenses(expense_date: str):
    try:
        # Strip extra spaces/newlines and convert to date
        expense_date_obj = date.fromisoformat(expense_date.strip())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    expenses = db_helpers.fetch_expenses_for_date(expense_date_obj)

    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date ,expenses: List[Expense]):
    try:
        expense_date_obj = date.fromisoformat(expense_date.strip())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    db_helpers.delete_expenses_for_date(expense_date_obj)
    for expense in expenses:
        db_helpers.insert_expense(expense_date_obj, expense.amount, expense.category, expense.notes)
    return {"message": "Expense added successfully"}

@app.post("/analytics")
def get_analytics(date_range :DateRange):
    data = db_helpers.fetch_expense_summary(date_range.start_date, date_range.end_date)

    if data is None:
        raise HTTPException(status_code=500,detail="Failed to retrieve expense summary for database")

    # total = sum([row["total"] for row in data])
    try:
        total = sum(row["total"] for row in data)
    except KeyError:
        raise HTTPException(
            status_code=500,
            detail="Invalid data format returned from database"
        )

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total !=0 else 0
        breakdown[row["category"]] ={
            "total" :row['total'],
            "percentage" :percentage
        }

    return breakdown

