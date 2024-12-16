from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt 
import my_secrets
from database import Database
import os
import sys
from socket import *
import json

#misc Fungtions
######################################################################################################################################################

#fungtion to send data in a digestebel form about pil despensing to a pill despenser
def dispense(pills, ip):
    pills = json.dumps(pills)
    str_pills = str(pills)
    serverName = ip
    serverPort = 12000
    clintSocket = socket(AF_INET, SOCK_DGRAM)
    clintSocket.sendto(str_pills.encode("utf-8"), (serverName, serverPort))
    print(pills)


def ping(ip):
    param = '-n' if sys.platform.lower() == 'win32' else '-c'
    hostname = ip  # example
    response = os.system(f"ping {param} 1 {hostname}")
    
    # and then check the response...
    if response == 0:
        print(f"{hostname} is up!")
        return("Is Up")
    else:
        print(f"{hostname} is down!")
        return("Is Down")

#flask misc setup
######################################################################################################################################################

remote_db = Database(
	my_secrets.db_ip,
    my_secrets.db_user,
    my_secrets.db_password,
    my_secrets.db_db
)

#flask login setup
######################################################################################################################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<username>:<password>@<host>/<database_name>"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{my_secrets.db_user}:{my_secrets.db_password}@{my_secrets.db_ip}/{my_secrets.db_db}"
app.config["SECRET_KEY"] = my_secrets.secret_key
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

#make entys for remote db?
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.init_app(app)
    bcrypt = Bcrypt(app) 
    db.create_all()


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
				username=request.form.get("username")).first()
			if bcrypt.check_password_hash(user.password, request.form.get("password")):
				login_user(user)
				return redirect(url_for("menu"))
		except:
			return render_template('forside.html',warn = 'WRONG PASSWORD OR USERNAME')
	return render_template('forside.html', warn = 'none')
        #^^^^fix login page^^^^

@app.route("/menu")
def menu():
	#get data from database to be able to list all mashines in db an use the id as a link to machine page
	maskiner = remote_db.get("SELECT * FROM maskiner")
	return render_template('menu.html',maskiner = maskiner, maskiner_len = len(maskiner))

@app.route("/maskine/<int:id>", methods=["GET", "POST"])
def maskine(id):
	maskin = remote_db.get_where("SELECT * FROM maskiner WHERE id = (%s)",(id,))
	name = maskin[0][1]
	ip = maskin[0][2]
	up = ping(ip)
    #despense handeling to handle wene a post reqest wiyh pills come in
	if request.method == "POST":
		piller = remote_db.get("SELECT * FROM piller")
		#digest input from site to only the pills that hase to be despensted
		piller_for_dispense = []
		if request.form.get("date"):
			piller_for_dispense.append(request.form.get("datetime"))
		for pille in piller:
			pil = []
			amount = request.form.get(str(pille[0]))
			if int(amount) > 0:
				pil.append(pille[0])
				pil.append(request.form.get(str(pille[0])))
				piller_for_dispense.append(pil)
		
		dispense(piller_for_dispense, ip)
		return render_template('maskine.html', piller = piller, len_piller = len(piller), up = up, name = name)
    #site reqest for showing the site wene a nomal reqest soms in
	piller = remote_db.get("SELECT * FROM piller")
	return render_template('maskine.html', piller = piller, len_piller = len(piller), up = up, name = name)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))


## TEMP REMOVE WENNE NOT IN USE
@app.route('/make_user', methods=["GET", "POST"])
def make_user():
    if request.method == "POST":
        print(request.form.get("password"))
        hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        user = Users(username=request.form.get("username"), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template("make_user.html",warn = 'bruger_lavet')
    return render_template("make_user.html")

#end
######################################################################################################################################################
if __name__ == "__main__":
	app.run()