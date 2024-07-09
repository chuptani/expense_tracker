from datetime import datetime
from decimal import Decimal
from database import actions
from database.models import session, Person, ExpenseCategory, IncomeSource, Expense
from main import Ctx


ctx = Ctx(session)
# actions.add_income_source("salary", ctx)
# actions.add_category("food", ctx)
# session.commit()

# actions.add_expense(
#     date=ctx.current_date,
#     amount=Decimal(100.50),
#     account_id=1,
#     category_id=1,
#     notes="test expense",
#     ctx=ctx,
# )

actions.add_account("cash", ctx)
actions.add_account("card", ctx)
ctx.session.commit()
