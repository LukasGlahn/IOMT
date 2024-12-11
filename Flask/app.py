from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt 
from database_connector import DataBase
import hashlib
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql:///db.mysql"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

def make_creds(creds_list):
    creds = 0
    for i in creds_list:
        if i is None:
            i = 0
        else:
            i = int(i)
        creds = i | creds
    return creds


class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	creds = db.Column(db.Integer, nullable=False)

storage_db = DataBase('database/storage.db')

db.init_app(app)
bcrypt = Bcrypt(app) 

with app.app_context():
	db.create_all()


#jinja filters
def bitwise_and(a, b):
    return int(a) & int(b)

app.jinja_env.filters['bitwise_and'] = bitwise_and

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		try:
			user = Users.query.filter_by(
				username=request.form.get("brugernavn")).first()
			if bcrypt.check_password_hash(user.password, request.form.get("kode")):
				login_user(user)
				return redirect(url_for("menu"))
		except:
			return render_template('forside.html',warn = 'WRONG PASSWORD OR USERNAME')
	return render_template('forside.html', warn = 'none')

@app.route("/menu")
def menu():
	return render_template('menu.html')

@app.route('/dosehub1', methods=["GET", "POST"])
def dosehub1():
	if request.method == "POST":
		creds = make_creds((request.form.get("admin"),request.form.get("opret_gest"),request.form.get("scan")))
		user = Users(username=request.form.get("username"),
					password=bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8'),
					creds=creds)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("admin"))
	return render_template("dosehub1.html")

@app.route("/dosehub2")
def dosehub2():
	logout_user()
	return redirect(url_for("index"))

@app.route("/dosehub3")
def dosehub3():
	return render_template("dosehub3.html")

@app.route("/dosehub4")
def dosehub4(qr_nr):
	bagage_data = storage_db.get_databace_data(f'SELECT gestid FROM bagage WHERE id IS {qr_nr}')
	gestid = bagage_data[0][0]
	if gestid is None:
		return render_template("dosehub4.html",warn = 'TAG HAS NO DATA')
	else:
		gest_data = storage_db.get_databace_data(f'SELECT * FROM gest WHERE id IS {gestid}')
		return render_template("bagage.html",gest_data = gest_data, qr_nr = qr_nr,warn = 'none')

@app.route("/bagage_udlevering/<qr_nr>/", methods=["GET", "POST"])
def bagage_udlevering(qr_nr):
	gestid = storage_db.get_databace_data(f'SELECT id FROM gest WHERE uid IS "{qr_nr}"')
	print(gestid)
	if request.method == "POST":
		info = 'NOTHING WAS DONE'
		gestid = gestid[0][0]
		gest_bagage = storage_db.get_databace_data(f'SELECT id FROM bagage WHERE gestid IS {gestid}')
		bagage_list = []
		for bagage in gest_bagage:
			bag = request.form.get(str(bagage[0]))
			print(type(bag))
			if type(bag) == str:
				info = 'BAG(S) CHECKED OUT SUCCESFULLY'
				print(bag)
				storage_db.add_to_databace(f'UPDATE bagage SET gestid = NULL WHERE id = {bag};',())
			else:
				bagage_list.append(bagage[0])
		if len(bagage_list) == 0:
			storage_db.add_to_databace(f'DELETE FROM gest WHERE id = {gestid};',())
			info = 'GUEST CHECKED OUT'
		return render_template("bagage_udlevering.html",warn = 'none',bagage_list = bagage_list, bagage_list_len = len(bagage_list),info = info)
	elif len(gestid) == 0:
		return render_template("bagage_udlevering.html",warn = 'GUEST DOES NOT EXIST')
	else:
		gestid = gestid[0][0]
		gest_bagage = storage_db.get_databace_data(f'SELECT id FROM bagage WHERE gestid IS {gestid}')
		bagage_list = []
		for bagage in gest_bagage:
			bagage_list.append(bagage[0])
		return render_template("bagage_udlevering.html",warn = 'none', bagage_list = bagage_list, bagage_list_len = len(bagage_list), info = 'none')



if __name__ == "__main__":
	app.run()