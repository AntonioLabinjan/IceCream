from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Icecream2" # možemo napisati doslovno bilo koji secret key; bitno da ga imamo

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AN1246A301JA@localhost/Icecream' # OVDJE UNOSITE SVOJU MYSQL ŠIFRU
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# KLASE
class IceCream(db.Model):
    icecream_id = db.Column(db.Integer, primary_key = True)
    icecream_name = db.Column(db.String(100))
    icecream_price = db.Column(db.Float)

    def __init__(self, icecream_id, icecream_name, icecream_price):
        self.icecream_id = icecream_id
        self.icecream_name = icecream_name
        self.icecream_price = icecream_price

# RUTE
@app.route('/')
def Index():
    all_icecreams = IceCream.query.all()
    return render_template("index.html", icecreams=all_icecreams)

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
    
@app.route('/delete_icecream/<int:icecream_id>/', methods=['GET', 'POST'])
def delete_icecream(icecream_id):
    my_icecream = IceCream.query.get(icecream_id)

    if my_icecream is not None:
        db.session.delete(my_icecream)
        db.session.commit()
        flash("ICE CREAM HAS BEEN DELETED SUCCESSFULLY AT: " + datetime.now().strftime("%H:%M"))
    else:
        flash("Ice cream not found with ID: " + str(icecream_id))

    return redirect(url_for('Index'))

@app.route('/total_icecream_price')
def total_icecream_price():
    all_icecreams = IceCream.query.all()
    total_price = sum(icecream.icecream_price for icecream in all_icecreams)
    flash(f"Total Ice Cream Price: €{total_price:.2f}", "total_price")
    return redirect(url_for('Index'))

@app.route('/average_icecream_price')
def average_icecream_price():
    all_icecreams = IceCream.query.all()
    
    if not all_icecreams:
        flash("No ice creams found.", "average_price")
        return redirect(url_for('Index'))
    
    total_price = sum(icecream.icecream_price for icecream in all_icecreams)
    average_price = total_price / len(all_icecreams)
    
    flash(f"Average Ice Cream Price: €{average_price:.2f}", "average_price")
    return redirect(url_for('Index'))

@app.route('/total_icecream_count')
def total_icecream_count():
    total_count = IceCream.query.count()
    flash(f"Total Ice Cream Count: {total_count}", "total_count")
    return redirect(url_for('Index'))


if (__name__ == "__main__"):
    app.run(debug=True)

