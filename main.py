from flask import Flask, render_template, request,redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Optional
from datetime import  datetime
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location (Google Maps URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 10PM', validators=[DataRequired()])
    coffee_rating = StringField('Coffee Rating (Optional)', validators=[Optional()])
    wifi_rating = StringField('Wifi Strength (Optional)', validators=[Optional()])
    power_rating = StringField('Power Socket Availability (Optional)', validators=[Optional()])
    submit = SubmitField('Submit')

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

def emoji_rating(symbol, count):
    """Helper to repeat emoji based on number."""
    return symbol * int(count)

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Convert numbers to repeated emojis
        coffee_rating = emoji_rating("☕", form.coffee_rating.data)
        wifi_rating = emoji_rating("💪", form.wifi_rating.data)
        power_rating = emoji_rating("🔌", form.power_rating.data)

        with open('cafe-data.csv', mode='a', encoding='utf8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open_time.data,
                form.close_time.data,
                coffee_rating,
                wifi_rating,
                power_rating
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
