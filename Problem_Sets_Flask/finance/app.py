import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT * FROM stocks WHERE users_id = ?", session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = usd(user[0]["cash"])
    return render_template("index.html", stocks=stocks, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # checks if the user inputted a valid stock within their budget
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        # validates the symbol
        if not request.form.get("symbol") or stock == None:
            return apology("Invalid Symbol")

        # validates the number of shares entered
        if not request.form.get("shares") or not request.form.get("shares").isnumeric():
            return apology("Shares must be a number")
        if float(request.form.get("shares")) <= 0 or float(request.form.get("shares")) % 1 != 0:
            return apology("Shares must be an integer")

        # calculates the total based on the symbol and number of shares
        total = stock["price"] * int(request.form.get("shares"))

        # amount of cash the user has
        users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = users[0]["cash"]

        # ensures that the user has enough cash
        if total > cash:
            return apology("Can't Afford")

        # gets the row for the user and their symbol
        row = db.execute("SELECT * FROM stocks WHERE users_id = ? AND symbol = ?",
                         session["user_id"], request.form.get("symbol"))

        # if the user had previously bought stock with that symbol
        if len(row) == 1:
            # the number of shares and total price get updated
            shares_updated = int(row[0]["shares"]) + int(request.form.get("shares"))
            total_updated = stock["price"] * shares_updated
            db.execute("UPDATE stocks SET shares = ?, total = ? WHERE users_id = ? AND symbol = ?",
                       shares_updated, usd(total_updated), session["user_id"], request.form.get("symbol"))

        # if the user had not previously bought stock with that symbol
        else:
            db.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?)", session["user_id"], request.form.get(
                "symbol"), request.form.get("shares"), usd(stock["price"]), usd(total))

        # the transaction is made
        cash -= total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        # buy action gets added to the history
        db.execute("INSERT INTO history (users_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("symbol"), request.form.get("shares"), usd(stock["price"]))

        # the user is redirected to the home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get the history for the user
    history_log = db.execute("SELECT * FROM history WHERE users_id = ?", session["user_id"])
    return render_template("history.html", history_log=history_log)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change user's password"""
    if request.method == "POST":
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not request.form.get("username") or request.form.get("username") != user[0]["username"]:
            return apology("Must provide username, 403")
        if not request.form.get("new_password"):
            return apology("must provide new password", 403)
        if not request.form.get("confirmation") or request.form.get("new_password") != request.form.get("confirmation"):
            return apology("New passwords do not match")

        hash = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])
        return redirect("/")
    else:
        return render_template("change.html")


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
    if request.method == "POST":
        # gets the stock
        stock = lookup(request.form.get("symbol"))

        # if the user typed an invalid stock
        if stock == None:
            return apology("Invalid Symbol")
        else:
            # the quote is printed onto the screen
            stock["price"] = usd(stock["price"])
            return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # if no username is provided
        if not request.form.get("username"):
            return apology("must provide username")

        # if no password is provided
        if not request.form.get("password"):
            return apology("must provide password")

        # if confirmation password is not retyped or confirmation doesn't match the original password
        if not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # generate hash of password
        hash = generate_password_hash(request.form.get("password"))

        # check if the username is valid
        try:
            # adds new user to database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       request.form.get("username"), hash)
        except ValueError:
            return apology("Username already exists")

        id = db.execute(
            "SELECT id FROM users WHERE username = ? AND hash = ?", request.form.get("username"), hash)
        session["user_id"] = id[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # list of all stocks the user owns
    stocks = db.execute("SELECT symbol FROM stocks WHERE users_id = ?", session["user_id"])
    owned_stocks = []
    for stock in stocks:
        owned_stocks.append(stock["symbol"])

    if request.method == "POST":
        # validates the symbol
        if not request.form.get("symbol"):
            return apology("Missing Symbol")
        if request.form.get("symbol") not in owned_stocks:
            return apology("Invalid Symbol")

        # validates the number of shares the user wants to sell
        row = db.execute("SELECT * FROM stocks WHERE users_id = ? AND symbol = ?",
                         session["user_id"], request.form.get("symbol"))
        shares = row[0]["shares"]
        if int(request.form.get("shares")) > int(shares):
            return apology("Too many shares")
        if int(request.form.get("shares")) < 1:
            return apology("Shares must be positive")

        # updates the number of shares and total price of those shares
        shares -= int(request.form.get("shares"))
        price = lookup(request.form.get("symbol"))
        total = price["price"] * int(shares)
        db.execute("UPDATE stocks SET shares = ?, total = ? WHERE users_id = ? AND symbol = ?",
                   shares, usd(total), session["user_id"], request.form.get("symbol"))

        # updates the amount of cash the user has
        users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = users[0]["cash"]
        cash += (price["price"] * int(request.form.get("shares")))
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        # if the user sells all of its shares for a company, it doesn't show up on the table
        db.execute("DELETE FROM stocks WHERE shares = 0")

        # sell action gets added to the history
        shares_change = -1 * int(request.form.get("shares"))
        look = lookup(request.form.get("symbol"))
        price = look["price"]
        db.execute("INSERT INTO history (users_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("symbol"), shares_change, usd(price))

        # redirect to the home page
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)
