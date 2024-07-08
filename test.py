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

# actions.delete_expense(1)

# actions.add_category("food")
# actions.delete_category(1)

# actions.add_account("cash")
# actions.add_account("card")
# for account in actions.get_accounts():
#     session.delete(account)
actions.add_income_source("dad")
session.commit()
