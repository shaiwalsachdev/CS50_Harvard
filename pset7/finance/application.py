from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    result = db.execute("SELECT * FROM netshares WHERE user_id = :id ",id=session["user_id"])
    
    net_evaluation = {}
    i = 0
    total = 0
    for r in result:
        look_quote = lookup(r["symbol"])
        shares = int(r["shares"])
        net_price_shares = float(shares * float(look_quote['price']))
        total = total + net_price_shares
        net_evaluation[i] = {}
        net_evaluation[i]['symbol']  = look_quote['symbol']
        net_evaluation[i]['name'] = look_quote['name']
        net_evaluation[i]['shares'] = str(r["shares"])
        net_evaluation[i]['price'] = str(usd(float(look_quote['price'])))
        net_evaluation[i]['Total'] = str(usd(net_price_shares))
        i = i + 1
        
    result_cash = db.execute("SELECT * from users where id = :id",id=session["user_id"])
    net_cash = result_cash[0]["cash"]
    
    net_evaluation[i] = {}
    net_evaluation[i]['symbol']  = "CASH"
    net_evaluation[i]['name'] = " "
    net_evaluation[i]['shares'] = " "
    net_evaluation[i]['price'] = " "
    net_evaluation[i]['Total'] = str(usd(net_cash))
    i = i + 1
    
    total = total + net_cash
    
    net_evaluation[i] = {}
    net_evaluation[i]['symbol']  = "Total_evaluation"
    net_evaluation[i]['name'] = " "
    net_evaluation[i]['shares'] = " "
    net_evaluation[i]['price'] = " "
    net_evaluation[i]['Total'] = str(usd(total))
    i = i + 1
    
    
    #print (total)
    #print (net_evaluation)
    
    return render_template("index.html",net_evaluation = net_evaluation)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("sharesnumber"):
            return apology("must provide no of shares")
        elif '.' in  request.form.get("sharesnumber"):
            return apology("No of shares is positive integer Invalid!!")
        elif not request.form.get("sharesnumber").isdigit():
            return apology("No of shares is positive integer Invalid!!")
        elif not int(request.form.get("sharesnumber")) > 0:
            return apology("No of shares is positive value Invalid!!")
            
        result_dict = lookup(request.form.get("symbol"))
        
        if result_dict == None:
            return apology("Symbol does not exist")
        
        result_cash = db.execute("SELECT * from users where id = :id",id=session["user_id"])
        net_cash = result_cash[0]["cash"]
        net_required = int(request.form.get("sharesnumber")) *  result_dict['price']
        if net_required > net_cash:
            return apology("Oops Don't Have enough Cash!!")
        
        
        #Update Cash
        net_cash = net_cash - net_required
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",cash= net_cash,id=session["user_id"])
        
        #Update History Tables
        
        db.execute("INSERT INTO  history(user_id,symbol,price,shares) VALUES(:id,:symbol,:price,:shares) ",id=session["user_id"],symbol=result_dict['symbol'],price=result_dict['price'],shares=request.form.get("sharesnumber"))
            
        #Check Whether user has shares for same symbol
        rows = db.execute("SELECT * FROM netshares WHERE user_id = :id AND symbol=:symbol",id=session["user_id"],symbol=result_dict['symbol'])
        #Update NetShares Table
        if len(rows) == 0:
            db.execute("INSERT INTO  netshares(user_id,symbol,shares) VALUES(:id,:symbol,:shares)",id=session["user_id"],symbol=result_dict['symbol'],shares=request.form.get("sharesnumber"))
        else:
            db.execute("UPDATE netshares SET shares=:shares WHERE user_id = :id AND symbol=:symbol",shares= int(request.form.get("sharesnumber"))+int(rows[0]['shares']),id=session["user_id"],symbol=result_dict['symbol'])
        return redirect(url_for("index"))
        
    else:
         return render_template("buy.html")
        
    
    #return apology("TODO")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    result = db.execute("SELECT * FROM history WHERE user_id = :id ",id=session["user_id"])
    net_evaluation = {}
    i = 0
    
    for r in result:
        look_quote = lookup(r["symbol"])
        net_evaluation[i] = {}
        net_evaluation[i]['symbol']  = r["symbol"]
        net_evaluation[i]['name'] = look_quote['name']
        net_evaluation[i]['shares'] = str(r["shares"])
        net_evaluation[i]['price'] = str(usd(float(r["price"])))
        net_evaluation[i]['Time'] = str(r['Time'])
        i = i + 1
    
    return render_template("history.html",net_evaluation=net_evaluation)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        if not request.form.get("money"):
            return apology("must provide money to add")
        elif not request.form.get("money").isdigit():
            return apology("money is positive integer Invalid!!")
        elif '.' in request.form.get("money"):
            return apology("money is positive integer Invalid!!")
        elif int(request.form.get("money")) < 0:
            return apology("Provide Positive Money")
        result_cash = db.execute("SELECT * from users where id = :id",id=session["user_id"])
        net_cash = result_cash[0]["cash"] + int(request.form.get("money"))
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",cash= net_cash,id=session["user_id"])
        return redirect(url_for("index"))
    else:
        return render_template("addcash.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("symbol is required")
        result_dict = lookup(request.form.get("symbol"))
        #print (result_dict)
        result = []
        result.append(("Name: ", result_dict['name']))
        result.append(("Price: ", usd(result_dict['price'])))
        result.append(("Symbol:  ", result_dict['symbol']))
        return render_template("quoted.html",result = result)
    
    else:
        return render_template("quote.html")
    
    #return apology("TODO")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        # ensure password was submitted
        elif not request.form.get("password1"):
            return apology("must provide confirm password")
        
        elif request.form.get("password") != request.form.get("password1"):
            return apology("passwords don't match")
        
        
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # if username exists
        if len(rows) == 1 :
            return apology("username already exists")
            
        #Insert data into users table
        db.execute("INSERT INTO users(username,hash) VALUES(:username,:hash)", username=request.form.get("username"),hash = pwd_context.encrypt(request.form.get("password")))
        
        
        #Now get the current user's id
        rows1 = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        # remember which user has logged in
        session["user_id"] = rows1[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

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

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        elif not request.form.get("oldpassword"):
            return apology("must provide old password")
            
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        # ensure password was submitted
        elif not request.form.get("password1"):
            return apology("must provide confirm password")
        
        elif request.form.get("password") != request.form.get("password1"):
            return apology("passwords don't match")
              
        
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        
        # if username exists no
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("oldpassword"), rows[0]["hash"]):
            return apology("invalid username and/or old password")
        
        print (rows[0]["id"])
        command = "Update users SET hash = '"+ str(pwd_context.encrypt(request.form.get("password")))+"' WHERE id = "+str(rows[0]["id"])
        #print (command)
        db.execute(command)
        '''
        #Update users table
        db.execute("UPDATE users SET hash = ':hash' WHERE id = :id", hash=str(pwd_context.encrypt(request.form.get("password")),id = str(rows[0]["id"])))
        '''
        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # redirect user to home page
        return redirect(url_for("index"))
        
        #return render_template("changepwd.html")
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepwd.html")
    
    #return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("sharesnumber"):
            return apology("must provide no of shares to sell")
        elif '.' in request.form.get("sharesnumber"):
            return apology("No of shares is positive integer Invalid!!")
        elif not request.form.get("sharesnumber").isdigit():
            return apology("No of shares is positive integer Invalid!!")
        elif not int(request.form.get("sharesnumber")) > 0:
            return apology("No of shares is positive value Invalid!!")
            
        result_dict = lookup(request.form.get("symbol"))
        
        if result_dict == None:
            return apology("Symbol does not exist")
        
        
        #Check No of Shares
        no_of_shares = db.execute("SELECT * FROM netshares WHERE user_id = :id AND symbol = :symbol",id=session["user_id"],symbol =request.form.get("symbol"))
        no_of_shares = int(no_of_shares[0]['shares'])
        if int(request.form.get("sharesnumber")) > no_of_shares:
            return apology("Sorry!! Don't Have Enough shares")
        
        result_cash = db.execute("SELECT * from users where id = :id",id=session["user_id"])
        net_cash = result_cash[0]["cash"]
        net_worth = int(request.form.get("sharesnumber")) *  result_dict['price']
        
        
        
        #Update Cash
        net_cash = net_cash + net_worth
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",cash= net_cash,id=session["user_id"])
        
        #Update History Tables
        
        db.execute("INSERT INTO  history(user_id,symbol,price,shares) VALUES(:id,:symbol,:price,:shares) ",id=session["user_id"],symbol=result_dict['symbol'],price=result_dict['price'],shares=(-1)*int(request.form.get("sharesnumber")))
            
        #Check Whether user has shares for same symbol
        rows = db.execute("SELECT * FROM netshares WHERE user_id = :id AND symbol=:symbol",id=session["user_id"],symbol=result_dict['symbol'])
        #Update NetShares Table
        if len(rows) == 0:
            db.execute("INSERT INTO  netshares(user_id,symbol,shares) VALUES(:id,:symbol,:shares)",id=session["user_id"],symbol=result_dict['symbol'],shares=request.form.get("sharesnumber"))
        else:
            db.execute("UPDATE netshares SET shares=:shares WHERE user_id = :id AND symbol=:symbol",shares= -int(request.form.get("sharesnumber"))+int(rows[0]['shares']),id=session["user_id"],symbol=result_dict['symbol'])
        return redirect(url_for("index"))
        
    else:
         return render_template("sell.html")
    #return apology("TODO")
