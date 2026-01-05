from fastapi import  FastAPI , HTTPException
from datetime import date
import db_helpers
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()


@app.get("/expenses/{expense_date}" ,response_model =List[Expense])
async def get_expenses(expense_date: date):
    expenses = db_helpers.fetch_expenses_for_date(expense_date)

    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date ,expenses: List[Expense]):
    db_helpers.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helpers.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

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

