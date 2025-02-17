import datetime
import calendar
from enum import Enum, auto


class Entry(Enum):
    EXPENSE = auto()
    CATEGORY = auto()
    INCOME = auto()
    SOURCE = auto()
    ACCOUNT = auto()
    PERSON = auto()
    PERSON_TRANSACTION = auto()


class Week:
    def __init__(self, date):
        self.date = date

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

    @property
    def start_date(self):
        # Start of the week (Monday)
        start = self.date - datetime.timedelta(days=self.date.weekday())
        return start

    @property
    def end_date(self):
        # End of the week (Sunday)
        end = self.date + datetime.timedelta(days=(6 - self.date.weekday()))
        return end

    @property
    def weekday_num(self):
        return self.date.weekday()

    @property
    def weekday(self):
        return self.weekdays[self.weekday_num]


class Month:
    def __init__(self, date):
        self.date = date
        self.number = date.month
        self.days = calendar.monthrange(date.year, date.month)[1]

    @property
    def start_date(self):
        # Start of the month
        start = self.date.replace(day=1)
        return start

    @property
    def end_date(self):
        # End of the month
        end = self.date.replace(day=self.days)
        return end


class Year:
    def __init__(self, date):
        self.date = date
        self.number = date.year

    @property
    def start_date(self):
        # Start of the year
        start = self.date.replace(month=1, day=1)
        return start

    @property
    def end_date(self):
        # End of the year
        end = self.date.replace(month=12, day=31)
        return end


class Ctx:
    def __init__(self, session=None, registry=None):

        self.entry = Entry
        self.session = session
        self.cli = registry

        self.now = datetime.datetime.now()

        self.today = self.now.date()
        self.this_week = Week(self.today)
        self.this_month = Month(self.today)
        self.this_year = Year(self.today)

        self.current_date = self.today
        self.current_week = Week(self.current_date)
        self.current_month = Month(self.current_date)
        self.current_year = Year(self.current_date)

        self.date_formats = ["%Y-%m-%d", "%m-%d", "%d"]

        self.session_additions = {ent: [] for ent in self.entry}
        self.session_deletions = {ent: [] for ent in self.entry}
        self.session_updates = {ent: [] for ent in self.entry}

    @property
    def ADDITIONS(self):
        return any(value for value in self.session_additions.values())

    @property
    def DELETIONS(self):
        return any(value for value in self.session_deletions.values())

    @property
    def UPDATES(self):
        return any(value for value in self.session_updates.values())

    def new_date(self, date=datetime.datetime.now().date()):
        self.current_date = date
        self.current_week.date = self.current_date
        self.current_month.date = self.current_date
        self.current_year.date = self.current_date

    def clear_session(self):
        self.session_additions = {ent: [] for ent in self.entry}
        self.session_deletions = {ent: [] for ent in self.entry}
        self.session_updates = {ent: [] for ent in self.entry}
