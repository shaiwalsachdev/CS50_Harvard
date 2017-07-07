from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for,jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime, date
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///foodiez.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dishesbycuisine")
@login_required
def dishesbycuisine():
    return render_template("dishesbycuisine.html")

@app.route("/fooditems")
@login_required
def fooditems():
    return render_template("fooditems.html")

@app.route("/recipes")
@login_required
def recipes():
    return render_template("recipes.html")

@app.route("/searchdish")
@login_required
def searchdish():
    return render_template("searchdish.html")

@app.route("/myprofile")
@login_required
def myprofile():
    return render_template("myprofile.html")


@app.route("/trackme")
@login_required
def trackme():
    return render_template("trackme.html")
    
    
@app.route("/myrecipes")
@login_required
def myrecipes():
    return render_template("myrecipes.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("form-username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("form-password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        #return redirect(url_for("index"))
        return render_template("dashboard.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()
    
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("form-username"))
    
        # if username exists
        if len(rows) == 1 :
            return apology("username already exists")
        
        # query database for username
        rows2 = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("form-email"))

        # if username exists
        if len(rows2) == 1 :
            return apology("email already exists")
            
        
        food_type = request.form['optradio']
        #Insert data into users table
        db.execute("INSERT INTO users(email,firstname,lastname,username,hash,food_type) VALUES(:email,:firstname,:lastname,:username,:hash,:food_type)",email=request.form.get("form-email"),firstname=request.form.get("form-firstname"), lastname=request.form.get("form-lastname"),  username=request.form.get("form-username"),hash = pwd_context.encrypt(request.form.get("form-password")),food_type = request.form['optradio'])
        
        
        #Now get the current user's id
        rows1 = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("form-username"))
        
        # remember which user has logged in
        session["user_id"] = rows1[0]["id"]
        session["food_type"] = request.form['optradio']
        
        # redirect user to home page
        #return redirect(url_for("index"))
        return render_template("login.html")
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
    #return apology("TODO")




@app.route("/changepwd", methods=["GET", "POST"])
def changepwd():
    """ChangePwd user."""
    # forget any user_id
    session.clear()
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("form-username"))
        
        
        # if username exists no
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("form-oldpassword"), rows[0]["hash"]):
            return apology1("invalid username and/or old password")
        
        print (rows[0]["id"])
        command = "Update users SET hash = '"+ str(pwd_context.encrypt(request.form.get("form-password")))+"' WHERE id = "+str(rows[0]["id"])
        #print (command)
        db.execute(command)
        '''
        #Update users table
        db.execute("UPDATE users SET hash = ':hash' WHERE id = :id", hash=str(pwd_context.encrypt(request.form.get("password")),id = str(rows[0]["id"])))
        '''
        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # redirect user to home page
        return redirect(url_for("login"))
        
        #return render_template("changepwd.html")
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepwd.html")
    
    #return apology("TODO")


@app.route("/dishes")
def dishes():
    """Display Popular Dishes."""

    # redirect user to login form
    return render_template("dishes.html")