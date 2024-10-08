from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import DataRequired


class EntryForRange(FlaskForm):
    entry_type = SelectField(
        "Options",
        choices=[
            ("", "Query"),
            ("expenses", "Expenses"),
            ("categories", "Categories"),
            ("incomes", "Incomes"),
            ("sources", "Sources"),
            ("accounts", "Accounts"),
        ],
        validators=[DataRequired()],
        render_kw={
            "onload": "this.options[0].disabled = true, this.options[0].selected = true"
        },
    )

    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("View")
    months = SelectField(
        "Month",
        choices=[
            ("", "Month"),
            ("01", "January"),
            ("02", "February"),
            ("03", "March"),
            ("04", "April"),
            ("05", "May"),
            ("06", "June"),
            ("07", "July"),
            ("08", "August"),
            ("09", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
    )

    years = SelectField(
        "Year",
        choices=[("", "Year")] + [(str(year), str(year)) for year in range(2000, 2031)],
    )
