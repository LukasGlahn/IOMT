from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt 
import secrets

#flask login setup
######################################################################################################################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql:///db.mysql"
app.config["SECRET_KEY"] = secrets.secret_key
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

#make entys for remote db?
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

db.init_app(app)
bcrypt = Bcrypt(app) 


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

#routes
######################################################################################################################################################

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		try:
			user = Users.query.filter_by(
				username=request.form.get("brugernavn")).first()
			if Bcrypt.check_password_hash(user.password, request.form.get("kode")):
				login_user(user)
				return redirect(url_for("menu"))
		except:
			return render_template('forside.html',warn = 'WRONG PASSWORD OR USERNAME')
	return render_template('forside.html', warn = 'none')
        #^^^^fix login page^^^^

@app.route("/menu")
def menu():
	#get data for all dose hubs in db
	return render_template('menu.html')

@app.route('/make_user', methods=["GET", "POST"])
def make_user():
    if request.method == "POST" and current_user.is_authenticated:
        hashed_password = Bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        user = Users(username=request.form.get("username"), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template("make_user.html",warn = 'bruger_lavet')
    return render_template("make_user.html")

#end
######################################################################################################################################################
if __name__ == "__main__":
	app.run()