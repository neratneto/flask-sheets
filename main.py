import datetime
from flask import Flask, request, render_template
from sheetsapi import Sheets


# FLASK SERVER
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/revision", methods=['GET', 'POST'])
def revision():
    if request.method == 'GET':
        return render_template('revision.html')
    elif request.method == 'POST':
        game = request.form['game']
        boolean = request.form['checkbox']
        id = request.form['id']
        date = str(datetime.datetime.now())
        admin_password = request.form['admin_password']
        name = Sheets.checkID(id, worksheet="admins")

        if boolean is False:
            return render_template('response.html', response="revise the game")
        if (name == "null"):
            return render_template('response.html', response="admin not found")
        if (admin_password != Sheets.password):
            return render_template('response.html', response="wrong password")
        Sheets.createRow(name, game, date, worksheet="revisions")
        return render_template('response.html', response="success")


@app.route("/checkout", methods=['POST'])
def checkout():
    if request.method == 'POST':
        game = request.form['game']
        id = request.form['id']
        date = str(datetime.datetime.now())

        name = Sheets.checkID(id, worksheet="registers")
        if (name == "null"):
            return render_template('response.html', response="no register")
        Sheets.createRow(name, game, date, worksheet="checkouts")
        return render_template('response.html', response="success")


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        address = request.form['address']
        tel = request.form['tel']
        admin_password = request.form['admin_password']

        if (admin_password != Sheets.password):
            return render_template('response.html', response="worng password")
        Sheets.createRow(id, name, address, tel, worksheet="registers")
        return render_template('response.html', response="success")


if __name__ == "__main__":
    app.run()
