from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import sqlite3

# Configure application
app = Flask(__name__)
app.secret_key='jzhfguzf'

# Initialize connection to constellations database
try:
    connection = sqlite3.connect("/workspaces/120191963/project/cons.db", check_same_thread=False)
except:
    print('Cannot connect to database')


# Cursor
connection.row_factory = sqlite3.Row
crsr = connection.cursor()


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Nav pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/constellations")
def constellations():
    return render_template("constellations.html")


# Constellations
@app.route("/andromeda")
def andromeda():
    return render_template("andromeda.html")


@app.route("/aquarius")
def aquarius():
    return render_template("aquarius.html")


@app.route("/canismajor")
def canismajor():
    return render_template("canismajor.html")


@app.route("/cassiopeia")
def cassiopeia():
    return render_template("cassiopeia.html")


@app.route("/cepheus")
def cepheus():
    return render_template("cepheus.html")


@app.route("/cygnus")
def cygnus():
    return render_template("cygnus.html")


@app.route("/gemini")
def gemini():
    return render_template("gemini.html")


@app.route("/hercules")
def hercules():
    return render_template("hercules.html")


@app.route("/leo")
def leo():
    return render_template("leo.html")


@app.route("/orion")
def orion():
    return render_template("orion.html")


@app.route("/perseus")
def perseus():
    return render_template("perseus.html")


@app.route("/sagittarius")
def sagittarius():
    return render_template("sagittarius.html")


@app.route("/scorpius")
def scorpius():
    return render_template("scorpius.html")


@app.route("/ursamajor")
def ursamajor():
    return render_template("ursamajor.html")


@app.route("/virgo")
def virgo():
    return render_template("virgo.html")


# Search page
@app.route("/search", methods=['GET', 'POST'])
def search():

    # Create list for 'Constellation' dropdown:
    crsr.execute("SELECT constellation FROM cons ORDER BY constellation")
    result = [dict(row) for row in crsr.fetchall()]
    cons_to_select_lst = [i['constellation'] for i in result]
    cons_to_select_abc = []
    for i in cons_to_select_lst:
        if i not in cons_to_select_abc:
            cons_to_select_abc.append(i)

    # Create logic for request methods
    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        visibility = request.form.get("visibility")
        object_type = request.form.get("objecttype")
        cons_to_print = request.form.get("constellation")
        name = request.form.get("name")

        if difficulty:
            diff_sql = """
            SELECT *
            FROM cons
            WHERE difficulty = ?
            ORDER BY constellation
            """
            crsr.execute(diff_sql, (difficulty,))
            constellations = [dict(row) for row in crsr.fetchall()]
        elif visibility:
            visib_sql = """
            SELECT *
            FROM cons
            WHERE visibility = ?
            ORDER BY constellation
            """
            crsr.execute(visib_sql, (visibility,))
            constellations = [dict(row) for row in crsr.fetchall()]
        elif object_type:
            obj_sql = """
            SELECT *
            FROM cons
            WHERE objecttype
            LIKE '%' || ? || '%'
            ORDER BY constellation
            """
            crsr.execute(obj_sql, (object_type,))
            constellations = [dict(row) for row in crsr.fetchall()]
        elif cons_to_print:
            cons_to_print_sql = """
            SELECT *
            FROM cons
            WHERE constellation = ?
            ORDER BY constellation
            """
            crsr.execute(cons_to_print_sql, (cons_to_print,))
            constellations = [dict(row) for row in crsr.fetchall()]
        elif name:
            name_sql = """
            SELECT *
            FROM cons
            WHERE lower(name)
            LIKE '%' || ? || '%'
            ORDER BY constellation
            """
            crsr.execute(name_sql, (name.lower(),))
            constellations = [dict(row) for row in crsr.fetchall()]
        else:
            crsr.execute("SELECT * FROM cons ORDER BY constellation LIMIT 0")
            constellations = [dict(row) for row in crsr.fetchall()]
            flash('Please provide an object name')

        return render_template("search.html", constellations=constellations, cons_to_select=cons_to_select_abc)

    return render_template("search.html", cons_to_select=cons_to_select_abc)


# Login function
@app.route("/login", methods=['GET', 'POST'])
def login():

    # Create logic for request methods
    if request.method == 'POST':
        login_username = request.form.get("login-username")
        login_password = request.form.get("login-password")

        if not login_username:
            flash('Please provide a username')
            return redirect("/login")
        elif not login_password:
            flash('Please provide a password')
            return redirect("/login")
        else:
            crsr.execute("SELECT * FROM users WHERE username = ?", (login_username,))
            user = [dict(row) for row in crsr.fetchall()]

            if len(user) != 1 or not check_password_hash(user[0]["password"], login_password):
                flash('Invalid username and/or password')
                return redirect("/login")

            # Remember which user has logged in
            session["user_id"] = user[0]["user_id"]

            # Redirect user to observations page
            return redirect("/observations")

    return render_template("login.html")


# Register function
@app.route("/register", methods=['GET', 'POST'])
def register():
    crsr.execute("SELECT username FROM users")
    usernames = [dict(row) for row in crsr.fetchall()]
    usernames_list = []

    if len(usernames) != 0:
        for i in usernames:
            usernames_list.append(i['username'])

    if request.method == 'POST':
        name = request.form.get('register-username')
        password = request.form.get('register-password')
        confirmation = request.form.get('confirm-password')
        if not name:
            flash('Please provide a username')
            return redirect("/register")
        elif name in usernames_list:
            flash('Username already taken')
            return redirect("/register")
        elif not password:
            flash('Please provide a password')
            return redirect("/register")
        elif password != confirmation:
            flash('Password and confirmation don\'t match')
            return redirect("/register")
        else:
            hashed_pw = generate_password_hash(password)
            crsr.execute("INSERT INTO users (username, password) VALUES(?, ?)", (name, hashed_pw))
            connection.commit()
            return redirect("/login")

    return render_template("register.html")


# Log user out
@app.route("/logout")
def logout():

    session.clear()
    return render_template("logout.html")


# Observations page
@login_required
@app.route("/observations", methods=['GET'])
def observations():

    obs_sql2 = """
    SELECT
    observations.name,
    cons.constellation,
    cons.coordinates_ra,
    cons.coordinates_dec,
    cons.objecttype,
    cons.visibility,
    cons.difficulty
    FROM cons
    INNER JOIN observations
    ON cons.name = observations.name
    WHERE observations.user_id = ?
    """
    crsr.execute(obs_sql2, (session["user_id"], ))
    user_obs = [dict(row) for row in crsr.fetchall()]

    return render_template("observations.html", user_obs=user_obs)

@login_required
@app.route('/delete/<obs_name>', methods=['POST'])
def delete(obs_name):
    crsr.execute('DELETE from observations WHERE name = ? AND user_id = ?', (obs_name, session["user_id"]))
    connection.commit()

    return redirect("/observations")


@login_required
@app.route('/add/<constellation_name>', methods=['POST'])
def add(constellation_name):
    crsr.execute("INSERT INTO observations (name, user_id) VALUES(?, ?)", (constellation_name, session["user_id"], ))
    connection.commit()

    return redirect("/observations")



# Run server
if __name__ == '__main__':
    app.run()


