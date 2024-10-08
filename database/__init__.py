from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "sqlite+pysqlite:///database/expense_tracker.db"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

from . import models
from . import actions
