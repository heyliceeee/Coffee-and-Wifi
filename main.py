from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    """Form to add a cafe to the database"""
    cafe = StringField('Cafe name', validators=[DataRequired()]) # make the cafe name field required
    location = StringField('Location URL', validators=[DataRequired(), URL()]) # make the location URL field required and must be a valid URL
    open_time = StringField('Open time', validators=[DataRequired()]) # make the open time field required
    closing_time = StringField('Closing time', validators=[DataRequired()]) # make the closing time field required
    coffee_rating = SelectField('Coffee Rating', choices=[("☕️", "☕️"), ("☕️☕️", "☕️☕️"), ("☕️☕️☕️", "☕️☕️☕️"), ("☕️☕️☕️☕️", "☕️☕️☕️☕️"), ("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️")], validators=[DataRequired()]) # make the coffee rating field required
    wifi_rating = SelectField('Wifi Rating', choices=[        ("✘", "✘"),
        ("💪", "💪"),
        ("💪💪", "💪💪"),
        ("💪💪💪", "💪💪💪"),
        ("💪💪💪💪", "💪💪💪💪"),
        ("💪💪💪💪💪", "💪💪💪💪💪")], validators=[DataRequired()]) # make the wifi rating field required
    power_rating = SelectField('Power Outlet Rating', choices=[        ("✘", "✘"),
        ("🔌", "🔌"),
        ("🔌🔌", "🔌🔌"),
        ("🔌🔌🔌", "🔌🔌🔌"),
        ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
        ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")], validators=[DataRequired()]) # make the power rating field required
    submit = SubmitField('Submit') # make the submit button

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm() # create an instance of the form
    if form.validate_on_submit(): # if the form is submitted
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file: # open the file in append mode
            writer = csv.writer(csv_file) # create a csv writer
            writer.writerow([form.cafe.data, form.location.data, form.open_time.data, form.closing_time.data, form.coffee_rating.data,  form.wifi_rating.data, form.power_rating.data]) # write the form data to the csv file
        return redirect(url_for("cafes")) # redirect to the cafes page
    return render_template('add.html', form=form) # pass the form to the template


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data: # iterate through each row
            list_of_rows.append(row) # append each row to the list
    return render_template('cafes.html', cafes=list_of_rows) # pass the list of rows to the template


if __name__ == '__main__':
    app.run(debug=True)
