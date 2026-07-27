from pydantic import BaseModel , Field, model_validator , field_validator
from datetime import date
from enum import Enum
from datetime import date

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class TransactionCategory(str, Enum):
    salary = "salary"
    gift = "gift"
    food = "food"
    rent = "rent"
    transport = "transport"
    bills = "bills"
    tax = "tax"
    gym = "gym"

class Transaction(BaseModel):

    type : TransactionType 
    amount : int = Field(gt=0)
    category : TransactionCategory
    date_ : date
    
    @model_validator(mode= "after")
    def vlidate_category(self):
        if self.type == TransactionType.income :
            if self.category not in (
                TransactionCategory.salary,
                TransactionCategory.gift
            ):
                raise ValueError(
                    "Income can only have salary or gift, category"
                )
        if self.type == "expense" :
            if self.category not in (
                TransactionCategory.bills,
                TransactionCategory.food,
                TransactionCategory.gym,
                TransactionCategory.rent,
                TransactionCategory.tax,
                TransactionCategory.transport
                
            ):
                raise ValueError(
                    "Expense can only have bills, food, gym, rent, tax, transport"
                )
        return self
    
    @field_validator("date_")
    @classmethod
    def validate_date(cls, value:date):
        if value > date.today():
            raise ValueError("" \
            "Date cannot be in the future")
        return value
        

class TransactionResponse(BaseModel):
    id : int
    type : str
    amount : int 
    category : str
    date_ : date

class BalanceResponse(BaseModel):
    income : int
    expense : int
    balance : int