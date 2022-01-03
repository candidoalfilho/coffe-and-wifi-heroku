from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Cafe Location on Google Maps (URL)')
    open_time = StringField('Opening Time e.g. 8AM')
    closing_time = StringField('Closing Time e.g. 5:30PM')
    rating = SelectField('Coffee Rating', choices=[(0, '✘'),(1, '☕'), (2, '☕☕'),(3, '☕☕☕'),(4, '☕☕☕☕'),(5, '☕☕☕☕☕')])
    wifi_strength = SelectField('Wifi Strength Rating', choices=[(0, '✘'),(1, '💪'), (2, '💪💪'), (3, '💪💪💪'), (4, '💪💪💪💪'), (5, '💪💪💪💪💪')])
    sockets = SelectField('Power Socket Availability', choices=[(0, '✘'),(1, '🔌'), (2, '🔌🔌'), (3, '🔌🔌🔌'), (4, '🔌🔌🔌🔌'), (5, '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), nullable=False)
    location_url = db.Column(db.String(250), unique=True, nullable=False)
    open_time = db.Column(db.String(250), nullable=False)
    closing_time = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.String(250), nullable=False)
    wifi_strength = db.Column(db.String(250), nullable=False)
    sockets = db.Column(db.String(250), nullable=False)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafe(
            cafe=form.cafe.data,
            location_url = form.location_url.data,
            open_time = form.open_time.data,
            closing_time = form.closing_time.data,
            rating = form.rating.choices[int(form.rating.data)][1],
            wifi_strength = form.wifi_strength.choices[int(form.wifi_strength.data)][1],
            sockets = form.sockets.choices[int(form.sockets.data)][1]
        )
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        cafes = db.session.query(Cafe).all()
        list_of_rows = []
        for cafe in cafes:
            list_of_rows.append([cafe.cafe,cafe.location_url,cafe.open_time,cafe.closing_time,cafe.rating,cafe.wifi_strength,cafe.sockets])
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
