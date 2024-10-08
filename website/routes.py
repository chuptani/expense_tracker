import database as db
from context import Ctx
from flask import render_template

from . import app
from .forms import EntryForRange

ctx = Ctx()


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    form = EntryForRange()
    entries = None
    selected_option = None
    if form.validate_on_submit():
        print("Form is valid")
        start_date = form.start_date.data
        end_date = form.end_date.data
        selected_option = form.entry_type.data
        if selected_option == "expenses":
            entries = db.actions.get_expenses(start_date, end_date)
        elif selected_option == "incomes":
            entries = db.actions.get_incomes(start_date, end_date)
        elif selected_option == "categories":
            entries = db.actions.get_categories()
    return render_template(
        "view.html", choice=selected_option, entries=entries, form=form
    )


@app.route("/test")
def test_page():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)

