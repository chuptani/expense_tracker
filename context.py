import datetime


class Ctx:
    def __init__(self):
        self.weekdays = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }

        self.dayweeks = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6,
        }

        self.now = datetime.datetime.now()
        self.today = self.now.date()
        self.current_date = self.today
        self.weekday_num = self.today.weekday()
        self.weekday = self.weekdays[self.weekday_num]

        self.date_formats = ["%Y-%m-%d", "%m-%d", "%d"]

        self.session_additions = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }

        self.session_deletions = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }

        self.session_updates = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }

    def new_date(self, date=datetime.datetime.now().date()):
        self.current_date = date
        self.weekday_num = date.weekday()
        self.weekday = self.weekdays[self.weekday_num]

    def clear_session(self):
        self.session_additions = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }

        self.session_deletions = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }

        self.session_updates = {
            "expenses": [],
            "incomes": [],
            "accounts": [],
            "categorys": [],
            "sources": [],
            "persons": [],
        }
