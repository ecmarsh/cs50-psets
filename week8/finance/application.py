import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, pct

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user info & validate
    user_id = session.get("user_id")
    u_res = db.execute("SELECT * FROM users WHERE id = (:user_id)", user_id=user_id)
    if len(u_res) == 1:
        user = {
            "name": u_res[0]["username"],
            "cash": u_res[0]["cash"],
            "change": (int(u_res[0]["cash"]) - 10000)/10000
        }
    else:
        return apology("error accessing your account", 404)

    # Get transactions for user
    transactions = db.execute("SELECT symbol, "
                              "SUM(shares) AS total_shares, "
                              "SUM(shares * price) / NULLIF(SUM(shares), 0) AS avg_cost "
                              "FROM portfolio "
                              "WHERE (user_id = :user_id) "
                              "GROUP BY symbol",
                              user_id=user_id)

    # Save transaction data to send to template table
    positions = []
    for i in range(len(transactions)):
        if transactions[i]["total_shares"] != 0:
            positions.append({
                "symbol": transactions[i]["symbol"],
                "name": lookup(transactions[i]["symbol"])["name"],
                "shares": transactions[i]["total_shares"],
                "cost": transactions[i]["avg_cost"],
                "value": lookup(transactions[i]["symbol"])["price"],
                "total": transactions[i]["total_shares"] * lookup(transactions[i]["symbol"])["price"],
            })

    # Calculate users total account value
    total = user["cash"]
    for i in range(len(positions)):
        total += positions[i]["total"]

    return render_template("/index.html",
                           user=user,
                           positions=positions,
                           accountValue=total,
                           usd=usd,
                           pct=pct)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by search form via POST)
    if request.method == "POST":

        formSymbol = request.form.get("symbol")
        formShares = request.form.get("shares")

        # Ensure inputs are filled
        if not formSymbol:
            return apology("please enter a symbol", 400)
        elif not formShares:
            return apology("please enter shares to buy", 400)

        # Validate shares quantity
        if formShares:
            try:
                castedShares = float(formShares)
            except ValueError:
                return apology("please enter valid quantity int", 400)
        if castedShares < 1 or castedShares % 1 != 0:
            return apology("please enter valid quantity int", 400)

        # Fetch data & check response
        res = lookup(request.form.get("symbol"))
        if res == None:
            return apology("no symbols match your search", 400)

        # Variable assignment
        user_id = session.get("user_id")
        symbol = res['symbol']
        symbol_name = res['name']
        price = res['price']
        shares = int(formShares)
        total = price * shares

        # Ensure user match & save their current cash
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)
        if len(user) != 1:
            return apology("error accessing your account", 404)
        else:
            usersCash = user[0]['cash']
            updatedCash = usersCash - total

        # Check enough cash for purchase
        if usersCash < total:
            return apology("not enough cash for purchase", 400)

        # All test pass -> add it to user's portfolio
        db.execute("INSERT INTO portfolio (user_id, symbol, symbol_name, price, shares) "
                   "VALUES (:user_id, :symbol, :symbol_name, :price, :shares)",
                   user_id=user_id,
                   symbol=symbol,
                   symbol_name=symbol_name,
                   price=price,
                   shares=shares)

        # Update users cash
        db.execute("UPDATE users SET cash = (:updatedCash) WHERE id = (:user_id)",
                   updatedCash=updatedCash,
                   user_id=user_id)

        # Purchase complete, go to homepage
        return redirect("/")

    # User reached route via GET
    else:
        cash = db.execute("SELECT cash FROM users WHERE (id = :user_id)", user_id=session.get("user_id"))
        print()
        if len(cash) == 1:
            cb = cash[0]['cash']
        else:
            cb = 10000

        cb = usd(cb)
        return render_template("buy.html", cb=cb)


@app.route("/check")
def check():
    """Return true if username available, else false, in JSON format"""

    # Get data (username) sent to server
    username = request.args.get('username')

    # Check that username
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    if len(rows) > 0:
        return jsonify(False)

    return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Store user id to select
    user_id = session.get("user_id")

    # Get user transactions via user_id
    transQuery = db.execute("SELECT symbol, shares, symbol_name, price, stamp "
                            "FROM portfolio WHERE (user_id = :user_id)",
                            user_id=user_id)

    # Save transaction data to send to template table
    transactions = []
    for i in range(len(transQuery)):
        q = transQuery[i]["shares"]
        if q < 0:
            t_type = "sold"
        elif q > 0:
            t_type = "bought"
        else:
            t_type = "-"

        # Extract values from time stamp string
        date_time_obj = datetime.datetime.strptime(transQuery[i]["stamp"], '%Y-%m-%d %H:%M:%S')

        transactions.append({
            "date": date_time_obj.date(),
            "time": date_time_obj.time(),
            "symbol": transQuery[i]["symbol"],
            "name": transQuery[i]["symbol_name"],
            "shares": abs(transQuery[i]["shares"]),
            "price": usd(transQuery[i]["price"]),
            "type": t_type
        })

    # Render table
    return render_template("/history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by search form via POST)
    if request.method == "POST":

        # Ensure symbol is entered
        if not request.form.get("symbol"):
            return apology("please enter a search term", 400)

        # Lookup matches
        symbol = request.form.get("symbol")
        res = lookup(symbol)

        # If valid symbol, render results
        if res == None:
            return apology("no symbols match your search", 400)
        else:
            return render_template("/quoted.html", stock=res, usd=usd, pct=pct)

    # User reached route via GET (to initiate a search)
    else:
        return render_template("/quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username & password were submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("confirmation") or request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation must match", 400)

        # Query database for username and check that doesn't exsit
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) > 0:
            return apology("sorry that username is taken", 400)

        # All tests pass, insert into table using hashed password
        db.execute(
            "INSERT INTO users (username, hash) "
            "VALUES (:username, :password)",
            username=request.form.get("username"),
            password=generate_password_hash(request.form.get("password"),
                                            method='pbkdf2:sha256',
                                            salt_length=8))

        # Attempt setting up new session for user
        session_id = db.execute("SELECT id FROM users WHERE username = :username",
                                username=request.form.get("username"))

        # Log in for them only if no errors (so duplicate username not an issue)
        if len(session_id) == 1:
            session["user_id"] = session_id[0]["id"]

        # Redirect to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Get user id for queries
        user_id = session.get("user_id")

        # Ensure shares is entered and a valid number
        if not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("please select a valid number of shares", 403)

        # Store form info
        sharesRequested = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        # Get user transactions
        sharesQuery = db.execute("SELECT SUM(shares) AS total_shares "
                                 "FROM portfolio "
                                 "WHERE user_id = :user_id AND (symbol = :symbol)",
                                 user_id=user_id,
                                 symbol=symbol)

        # Ensure queries were received & store actual shares
        if len(sharesQuery) != 1:
            return apology("error checking your information", 400)
        sharesActual = sharesQuery[0]["total_shares"]

        # Ensure user has that many shares for respective symbol
        updatedShares = sharesActual - sharesRequested
        if updatedShares < 0:
            return apology("you only own " + str(sharesActual) + " shares", 400)

        # Variables for checking/updating
        res = lookup(symbol)
        symbol_name = res['name']
        price = res['price']
        # Negative shares for selling
        shares = int(request.form.get("shares")) * -1
        total = price * shares

        # Validate user again & store their updated cash
        user = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if len(user) != 1:
            return apology("error accessing your account", 400)
        else:
            usersCash = user[0]['cash']
            updatedCash = usersCash - total

        # All test pass -> remove it to/from user's portfolio
        db.execute("INSERT INTO portfolio (user_id, symbol, symbol_name, price, shares) "
                   "VALUES (:user_id, :symbol, :symbol_name, :price, :shares)",
                   user_id=user_id,
                   symbol=symbol,
                   symbol_name=symbol_name,
                   price=price,
                   shares=shares)

        # Update users cash
        db.execute("UPDATE users SET cash = (:updatedCash) WHERE id = (:user_id)",
                   updatedCash=updatedCash,
                   user_id=user_id)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Validate user (cannot be on this page without valid session uid)
        user_id = session.get("user_id")

        # Ensure they have stocks to sell
        stockQuery = db.execute("SELECT symbol, SUM(shares) AS total_shares "
                                "FROM portfolio WHERE user_id = :user_id "
                                "GROUP BY symbol",
                                user_id=user_id)

        if len(stockQuery) < 1:
            stocks = []
        else:
            stocks = []
            for i in range(len(stockQuery)):
                if stockQuery[i]['total_shares'] > 0:
                    stocks.append(stockQuery[i]['symbol'])

        return render_template("sell.html",
                               stocks=stocks,
                               numberOfStocks=len(stocks))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
