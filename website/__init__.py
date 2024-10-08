from flask import Flask

app = Flask(__name__)
app.secret_key = "d6cd05528253f856e01a2c4249343fb5"

from . import routes
from . import forms
