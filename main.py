import random
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, IntegerField, BooleanField
from wtforms.validators import DataRequired, URL
import requests


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

class Find(FlaskForm):
    name = StringField("Type the cafe's name", validators=[DataRequired()])
    submit = SubmitField("Done")

class Update(FlaskForm):
    name = StringField("Type the cafe's name", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Done")
class AddCafe(FlaskForm):
    name = StringField("Write the cafe's name", validators=[DataRequired()])
    map_url = StringField("Paste map link", validators=[DataRequired(), URL()])
    img_url = StringField("Paste an image url", validators=[DataRequired(), URL()])
    location = StringField("Where is it?", validators=[DataRequired()])
    seats = IntegerField("How many seats?", validators=[DataRequired()])
    has_toilets = BooleanField("Does is have toilets?")
    has_wifi = BooleanField("Does is have WIFI?")
    has_sockets = BooleanField("Does is have sockets?")
    can_take_calls = BooleanField("Does it take calls?")
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DeleteCafe(FlaskForm):
    key = StringField("Write the super secret key", validators=[DataRequired()])
    name = StringField("Write the cafe's name", validators=[DataRequired()])
    submit = SubmitField("Submit")
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # def to_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}
# with app.app_context():
#     db.create_all()
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return render_template("cafe.html", cafe=random_cafe)


@app.route("/all")
def cafes():
    cafes = db.session.query(Cafe).all()
    return render_template("cafes.html", cafes=cafes)


@app.route("/search", methods=['GET', 'POST'])
def get_cafe_at_location():
    form = Find()
    if form.validate_on_submit():
        cafe = db.session.query(Cafe).filter_by(name=form.name.data).first()

        if cafe:
            return render_template("cafe.html", cafe=cafe)
    return render_template("search.html", form=form)


@app.route("/add", methods=['GET', 'POST'])
def post_new_cafe():
    form = AddCafe()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilets.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template("add.html", form=form)


@app.route("/update-price", methods=['GET', 'PATCH', 'POST', 'PUT'])
def patch_new_data():
    form = AddCafe()
    if form.validate_on_submit():
        cafe = Cafe.query.filter_by(name=form.name.data).first()
        if cafe:
            cafe.name = form.name.data,
            cafe.map_url = form.map_url.data,
            cafe.img_url = form.img_url.data,
            cafe.location = form.location.data,
            cafe.has_sockets = form.has_sockets.data,
            cafe.has_toilet = form.has_toilets.data,
            cafe.has_wifi = form.has_wifi.data,
            cafe.can_take_calls = form.can_take_calls.data,
            cafe.seats = form.seats.data,
            cafe.coffee_price = form.coffee_price.data
            with app.app_context():
                db.session.commit()
            return render_template("cafe.html", cafe=cafe)
    return render_template("update.html", form=form)


@app.route("/report-closed", methods=['GET', 'POST', 'DELETE'])
def delete_cafe():
    form = DeleteCafe()
    if form.validate_on_submit():
        if form.key.data == "SuperSecretKey":
            cafe = Cafe.query.filter_by(name=form.name.data).first()
            if cafe:
                db.session.delete(cafe)
                db.session.commit()
                return redirect(url_for('home'))


    return render_template("delete.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
