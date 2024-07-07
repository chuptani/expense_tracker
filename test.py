from datetime import datetime
from decimal import Decimal
from database import actions
from database.models import session, Person, ExpenseCategory, IncomeSource, Expense


# actions.add_expense(
#     datetime(2024, 7, 7).date(),
#     Decimal(100.50),
#     1,
#     1,
#     "test expense",
# )

actions.delete_expense(1)
session.commit()
