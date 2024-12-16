from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt 
import secrets
from database import Database

#misc Fungtions
######################################################################################################################################################

#fungtion to send data in a digestebel form about pil despensing to a pill despenser
def dispense(pills):
	print(pills)


#flask misc setup
######################################################################################################################################################

remote_db = Database(
	secrets.db_ip,
    secrets.db_user,
    secrets.db_password,
    secrets.db_db
)

#flask login setup
######################################################################################################################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
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
	#get data from database to be able to list all mashines in db an use the id as a link to machine page
	maskiner = remote_db.get("SELECT * FROM maskiner")
	return render_template('menu.html',maskiner = maskiner, maskiner_len = len(maskiner))

@app.route("/maskine/<int:id>", methods=["GET", "POST"])
def maskine(id):
	
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
		
		dispense(piller_for_dispense)
		return render_template('maskine.html', piller = piller, len_piller = len(piller))
    #site reqest for showing the site wene a nomal reqest soms in
	piller = remote_db.get("SELECT * FROM piller")
	return render_template('maskine.html', piller = piller, len_piller = len(piller))


## TEMP REMOVE WENNE NOT IN USE
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