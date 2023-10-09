from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Icecream27"  # You can insert any secret key here

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AN1246A301JA@localhost/Icecream'  # Insert your SQL password
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class IceCream(db.Model):
    icecream_id = db.Column(db.Integer, primary_key=True)
    icecream_name = db.Column(db.String(100))
    icecream_price = db.Column(db.Float)

    def __init__(self, icecream_id, icecream_name, icecream_price):
        self.icecream_id = icecream_id
        self.icecream_name = icecream_name
        self.icecream_price = icecream_price


@app.route('/')
def Index():
    all_icecreams = IceCream.query.all()
    return render_template("index.html", icecreams=all_icecreams) # ne želi nać template

@app.route('/insert_icecream', methods=['POST'])
def insert_icecream():
    if request.method == 'POST':
        icecream_id = request.form['icecream_id']
        icecream_name = request.form['icecream_name']
        icecream_price = request.form['icecream_price']

        my_icecream = IceCream(icecream_id, icecream_name, icecream_price)
        db.session.add(my_icecream)
        db.session.commit()

        flash("ICE CREAM HAS BEEN INSERTED SUCCESSFULLY AT: " + datetime.now().strftime("%H:%M"))

        return redirect(url_for('Index'))

@app.route('/update_icecream', methods=['GET', 'POST'])
def update_icecream():
    if request.method == 'POST':
        my_icecream = IceCream.query.get(request.form.get('icecream_id'))

        my_icecream.icecream_name = request.form['icecream_name']
        my_icecream.icecream_price = request.form['icecream_price']

        db.session.commit()
        flash("ICE CREAM HAS BEEN UPDATED SUCCESSFULLY AT: " + datetime.now().strftime("%H:%M"))

        return redirect(url_for('Index'))

@app.route('/delete_icecream/<icecream_id>/', methods=['GET', 'POST'])
def delete_icecream(icecream_id):
    my_icecream = IceCream.query.get(icecream_id)
    db.session.delete(my_icecream)
    db.session.commit()
    flash("ICE CREAM HAS BEEN DELETED SUCCESSFULLY AT: " + datetime.now().strftime("%H:%M"))

    return redirect(url_for('Index'))

if (__name__ == "__main__"):
    app.run(debug=True)