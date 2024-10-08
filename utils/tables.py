from rich.table import Table, box


class ExpensesTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Date", justify="center")
        self.add_column("Amount", justify="right")
        self.add_column("Notes", justify="center")
        self.add_column("Category", justify="center")
        self.add_column("Account", justify="center")

    def add_entry(self, expense, color=""):
        self.add_row(
            f"[{color}]" + str(expense.id),
            f"[{color}]" + str(expense.date.strftime("%b %d, %Y (%a)")),
            f"[{color}]" + str(expense.amount),
            f"[{color}]" + expense.notes,
            f"[{color}]" + expense.category.name,
            f"[{color}]" + expense.account.name,
        )


class CategoriesTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Name", justify="center")

    def add_entry(self, category, color=""):
        self.add_row(
            f"[{color}]" + str(category.id),
            f"[{color}]" + category.name,
        )


class IncomesTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Date", justify="center")
        self.add_column("Amount", justify="right")
        self.add_column("Account", justify="center")
        self.add_column("Source", justify="center")
        self.add_column("Notes")

    def add_entry(self, income, color=""):
        self.add_row(
            f"[{color}]" + str(income.id),
            f"[{color}]" + str(income.date.strftime("%b %d, %Y (%a)")),
            f"[{color}]" + str(income.amount),
            f"[{color}]" + income.account.name,
            f"[{color}]" + income.source.name,
            f"[{color}]" + income.notes,
        )


class SourcesTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Name", justify="center")

    def add_entry(self, source, color=""):
        self.add_row(
            f"[{color}]" + str(source.id),
            f"[{color}]" + source.name,
        )


class AccountsTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Name", justify="center")
        self.add_column("Balance", justify="right")

    def add_entry(self, account, color=""):
        self.add_row(
            f"[{color}]" + str(account.id),
            f"[{color}]" + account.name,
            f"[{color}]" + str(account.balance),
        )


class PersonsTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Name", justify="center")

    def add_entry(self, person, color=""):
        self.add_row(
            f"[{color}]" + str(person.id),
            f"[{color}]" + person.name,
        )


class PersonTransactionsTable(Table):
    def __init__(self):
        super().__init__(
            box=box.MINIMAL,
            show_edge=False,
            caption_justify="left",
            # expand=True,
        )
        self.add_column("ID", justify="right")
        self.add_column("Date", justify="center")
        self.add_column("Amount", justify="right")
        self.add_column("Person", justify="center")
        self.add_column("Notes")

    def add_entry(self, person_transaction, color=""):
        self.add_row(
            f"[{color}]" + str(person_transaction.id),
            f"[{color}]" + str(person_transaction.date.strftime("%b %d, %Y (%a)")),
            f"[{color}]" + str(person_transaction.amount),
            f"[{color}]" + person_transaction.person.name,
            f"[{color}]" + person_transaction.notes,
        )
