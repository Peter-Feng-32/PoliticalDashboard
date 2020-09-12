from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    user = {"username":"Coypirus"}
    return render_template('home.html', user = user)


@app.route("/bd")
def bd():
    return render_template("bd.html")


@app.route('/tips')
def tips():
    return render_template("tips.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/pn')
def pn():
    return render_template("pn.html")

