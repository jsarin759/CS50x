from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///trackify.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        # if no username is provided
        if not request.form.get("username"):
            flash('Missing Username.', 'danger')
            return render_template("login.html")
        # if no password is provided
        if not request.form.get("password"):
            flash('Missing Password.', 'danger')
            return render_template("login.html")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash('Invalid username and/or password.', 'danger')
            return render_template("login.html")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        flash('Hello! Here are your assignments', 'primary')
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")

@app.route("/forgot_pass", methods=["GET", "POST"])
def forgot_pass():
    if request.method == "POST":
        # get's the user's information
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # if there is no username inputted or the username is not correct
        if not request.form.get("username") or request.form.get("username") != user[0]["username"]:
            flash('Missing Username.', 'danger')
            return render_template("forgot_pass.html")

        # if there is no password inputted
        if not request.form.get("new_password"):
            flash('Missing a new password.', 'danger')
            return render_template("forgot_pass.html")

        # if no confirmation password is inputed or the new confirmation password doesn't match the new password
        if not request.form.get("confirmation") or request.form.get("new_password") != request.form.get("confirmation"):
            flash('Passwords do not match.', 'danger')
            return render_template("forgot_pass.html")

        # generates a password hash from the inputted password
        hash = generate_password_hash(request.form.get("new_password"))

        # updates the password
        db.execute("UPDATE users SET hash = ? WHERE username = ?", hash, request.form.get("username"))

        # returns a message
        flash('Password has been changed. Please login to continue.', 'success')
        return redirect("/login")
    else:
        # displays the page
        return render_template("forgot_pass.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # if no username is provided
        if not request.form.get("username"):
            flash('Missing Username.', 'danger')
            return render_template("register.html")

        # if no password is provided
        if not request.form.get("password"):
            flash('Missing Password.', 'danger')
            return render_template("register.html")

        # if confirmation password is not retyped or confirmation doesn't match the original password
        if not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            flash('Passwords do not match.', 'danger')
            return render_template("register.html")

         # generate hash of password
        hash = generate_password_hash(request.form.get("password"))

        # check if the username is valid
        try:
            # adds new user to database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       request.form.get("username"), hash)
        except ValueError:
            flash('Username already exists. Please login.', 'danger')
            return render_template("register.html")

        return redirect("/login")
    else:
        # displays the page
        return render_template("register.html")

@app.route("/update_status", methods=["GET", "POST"])
def update_status():
    # gets the data from the dropdown the user inputted
    data = request.get_json()
    name = data.get('name')
    status = data.get('statusTXT')
    # updates the status for the particular assignment
    db.execute("UPDATE assignments SET status = ? WHERE name = ?", status, name)
    return jsonify({
        "name": name,
        "statusTXT": status
    })

@app.route("/", methods=["GET", "POST"])
def index():
    # get's the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of possible statuses for an assignment
    statuses = ["Not Started", "In Progress", "Completed", "Submitted"]

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # the amount of assignments the user has
    length = len(db.execute("SELECT * FROM assignments WHERE users_id = ? ORDER BY remaining_time", session["user_id"]))

    # For each assignment, it gets its id, due date, and time which it is due
    due_dates_and_times = db.execute("SELECT id, due_date, due_time, name FROM assignments WHERE users_id = ?", session["user_id"])
    for i in range(length):
        assign_id = due_dates_and_times[i]["id"]
        due_date = due_dates_and_times[i]["due_date"]
        due_time = due_dates_and_times[i]["due_time"]
        assign_name = due_dates_and_times[i]["name"]

        # Utilized ChatGPT to display live countdown of days (not factoring in the time the assignment is due)
        year = int(due_date[:4])
        month = 0
        if due_date[5] == 0:
            month = int(due_date[6:7])
        else:
            month = int(due_date[5:7])
        day = int(due_date[8:10])
        target_date = datetime(year, month, day)
        current_date = datetime.now()
        difference = target_date - current_date

        # factors in the time the assignment is due
        hour = int(due_time[:2])
        minute = int(due_time[3:5])
        clock_time = (3600 * hour) + (60 * minute)

        # calculates the time left until the assignment is due
        remaining_time = (difference.days * 86400) + difference.seconds + clock_time

        # displays the countdown in table
        if remaining_time >= 0:
            db.execute("UPDATE assignments SET remaining_time = ? WHERE id = ?", remaining_time, assign_id)
        else:
            db.execute("UPDATE assignments SET remaining_time = 0 WHERE id = ?", assign_id)

        # orders the assignments by due date
        db.execute("WITH NumberedAssignments AS (SELECT *, ROW_NUMBER() OVER (ORDER BY remaining_time) AS new_row_number FROM assignments) UPDATE assignments SET row_num = NumberedAssignments.new_row_number FROM NumberedAssignments WHERE assignments.id = NumberedAssignments.id")

    # table of all assignments
    assignments = db.execute("SELECT * FROM assignments WHERE users_id = ? ORDER BY remaining_time", session["user_id"])
    return render_template("index.html", name=name, assignments=assignments, statuses=statuses, length=length)

@app.route("/subject", methods=["GET", "POST"])
def subject():
    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # get's the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"]) # CHANGE FALSE TO TRUE
    name = user[0]["username"]

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    if request.method == "POST":
        # if no subject was inputted
        if not request.form.get("subject"):
            flash('Invalid Subject', 'danger')
            return render_template("subject.html", name=name, subjects=users_subjects)

        # if the subject inputted already exists
        if request.form.get("subject").title() in users_subjects:
            flash('Subject Already Exists', 'danger')
            return render_template("subject.html", name=name, subjects=users_subjects)

        # get's the inputted subject
        subject = request.form.get("subject").title()

        # add's the recently inputted subject into the list of user's subjects
        users_subjects.append(subject)

        # inserts the subject into the assignments table
        db.execute("INSERT INTO subjects (users_id, subject) VALUES (?, ?)", session["user_id"], subject)

        # returns a confirmation message
        flash('Subject Successfully Added', 'success')
        return redirect("/")
    else:
        # displays the page
        return render_template("subject.html", name=name, subjects=users_subjects)

@app.route("/edit_subject", methods=["POST"])
def edit_subject():
    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        users_classes.append(room["class"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # if no subject was selected or the subject does not exist
    if not request.form.get("subject_name") or request.form.get("subject_name").title() not in users_subjects:
        flash('Invalid Subject', 'danger')
        return render_template("subject.html", name=name, subjects=users_subjects)

    # if a subject was selected to be edited, it's name gets updated
    if request.form.get("new_subject_name"):
        db.execute("UPDATE subjects SET subject = ? WHERE subject = ? AND users_id = ?", request.form.get("new_subject_name"), request.form.get("subject_name"), session["user_id"])
        db.execute("UPDATE subjects_and_classes SET subject = ? WHERE subject = ? AND users_id = ?", request.form.get("new_subject_name"), request.form.get("subject_name"), session["user_id"])
        db.execute("UPDATE assignments SET subject = ? WHERE subject = ? AND users_id = ?", request.form.get("new_subject_name"), request.form.get("subject_name"), session["user_id"])

    # returns a confirmation message
    flash('Subject Successfully Edited', 'success')
    return redirect("/")

@app.route("/remove_subject", methods=["POST"])
def remove_subject():
    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        users_classes.append(room["class"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # if subject selected does not exist
    if request.form.get("subject_name") not in users_subjects:
        flash('Invalid Subject to Remove', 'danger')
        return render_template("subject.html", name=name, subjects=users_subjects)

    # if a subject was selected to be removed, the subject get's removed
    if request.form.get("subject_name"):
        db.execute("DELETE FROM subjects WHERE subject = ? AND users_id = ?", request.form.get("subject_name"), session["user_id"])
        db.execute("DELETE FROM subjects_and_classes WHERE subject = ? AND users_id = ?", request.form.get("subject_name"), session["user_id"])
        db.execute("DELETE FROM assignments WHERE subject = ? AND users_id = ?", request.form.get("subject_name"), session["user_id"])

    # returns a confirmation message
    flash('Subject Successfully Removed', 'success')
    return redirect("/")

@app.route("/class", methods=["GET", "POST"])
def classes():
    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class, last_date FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        end_date = room["last_date"]
        year = int(end_date[:4])
        month = 0
        if end_date[5] == 0:
            month = int(end_date[6:7])
        else:
            month = int(end_date[5:7])
        day = int(end_date[8:10])
        target_date = datetime(year, month, day)
        current_date = datetime.now()
        difference = target_date - current_date
        if difference.days > 0:
            users_classes.append(room["class"])
        else:
            db.execute("DELETE FROM subjects_and_classes WHERE class = ?", room["class"])
            db.execute("DELETE FROM assignments WHERE class = ?", room["class"])

    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    if request.method == "POST":
        # if no subject was selected or the subject does not exist
        if not request.form.get("subject_of_class") or request.form.get("subject_of_class") not in users_subjects:
            flash('Invalid Subject for New Class', 'danger')
            return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

        # if no name was given
        if not request.form.get("class"):
            flash('Invalid New Class', 'danger')
            return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

        # if that class already exists
        if request.form.get("class").title() in users_classes:
            flash('Class Already Exists', 'danger')
            return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

        # if the last day of the class was not provided
        if not request.form.get("last_day"):
            flash('Missing Date for Last Day of Class', 'danger')
            return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

        # gets the information for the recently created class
        subject = request.form.get("subject_of_class").title()
        course = request.form.get("class").title()
        users_classes.append(course)
        last_date = request.form.get("last_day")
        print(last_date)

        # adds that class to the table of classes
        db.execute("INSERT INTO subjects_and_classes (users_id, class, subject, last_date) VALUES (?, ?, ?, ?)", session["user_id"], course, subject, last_date)

        # returns a confirmation message
        flash('Class Successfully Added', 'success')
        return redirect("/")
    else:
        # displays the page
        return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

@app.route("/edit_class", methods=["POST"])
def edit_class():
    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        users_classes.append(room["class"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # if the name of the class was not provided or the class does not exist
    if not request.form.get("class_name") or request.form.get("class_name") not in users_classes:
        flash('Invalid Class to Edit', 'danger')
        return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

    # if the subject was not provided or the subject does not exist
    if request.form.get("new_subject_for_class") not in users_subjects and request.form.get("new_subject_for_class"):
        flash('Invalid New Subject for Class', 'danger')
        return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

    # updates the subject for the class if a new subject was inputted
    if request.form.get("new_subject_for_class"):
        db.execute("UPDATE subjects_and_classes SET subject = ? WHERE class = ? AND users_id = ?", request.form.get("new_subject_for_class"), request.form.get("class_name"), session["user_id"])
        db.execute("UPDATE assignments SET subject = ? WHERE class = ? AND users_id = ?", request.form.get("new_subject_for_class"), request.form.get("class_name"), session["user_id"])

    # if the new name is the same as the old name
    if request.form.get("new_name") == request.form.get("class_name"):
        flash('New Class Name Must Be Different From the Old One', 'danger')
        return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

    # if a new name for the class was inputted
    if request.form.get("new_name"):
        db.execute("UPDATE subjects_and_classes SET class = ? WHERE class = ? AND users_id = ?", request.form.get("new_name"), request.form.get("class_name"), session["user_id"])
        db.execute("UPDATE assignments SET class = ? WHERE class = ? AND users_id = ?", request.form.get("new_name"), request.form.get("class_name"), session["user_id"])

    # if the class ended on a different day
    if request.form.get("new_last_day"):
        end_date = request.form.get("new_last_day")
        year = int(end_date[:4])
        month = 0
        if end_date[5] == 0:
            month = int(end_date[6:7])
        else:
            month = int(end_date[5:7])
        day = int(end_date[8:10])
        target_date = datetime(year, month, day)
        current_date = datetime.now()
        difference = target_date - current_date
        if difference.days > 0:
            if request.form.get("new_name"):
                db.execute("UPDATE subjects_and_classes SET last_date = ? WHERE class = ? AND users_id = ?", request.form.get("new_last_day"), request.form.get("new_name"), session["user_id"])
            else:
                db.execute("UPDATE subjects_and_classes SET last_date = ? WHERE class = ? AND users_id = ?", request.form.get("new_last_day"), request.form.get("class_name"), session["user_id"])
        else:
            db.execute("DELETE FROM subjects_and_classes WHERE class = ?", room["class"])
            db.execute("DELETE FROM assignments WHERE class = ?", room["class"])

    # returns a confirmation message
    flash('Class Updated Successfully', 'success')
    return redirect("/")

@app.route("/remove_class", methods=["POST"])
def remove_class():
    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's subjects
    users_subjects = []
    subjects = db.execute("SELECT subject FROM subjects WHERE users_id = ?", session["user_id"])
    for subject in subjects:
        users_subjects.append(subject["subject"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        users_classes.append(room["class"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # if the class name provided does not exist
    if request.form.get("class_name") not in users_classes:
        flash('Invalid Class to Remove', 'danger')
        return render_template("class.html", name=name, subjects=users_subjects, classes=users_classes)

    # if a class name was provided
    if request.form.get("class_name"):
        db.execute("DELETE FROM subjects_and_classes WHERE class = ? AND users_id = ?", request.form.get("class_name"), session["user_id"])
        db.execute("DELETE FROM assignments WHERE class = ? AND users_id = ?", request.form.get("class_name"), session["user_id"])

    # prints a confirmation message
    flash('Class Removed Successfully', 'success')
    return redirect("/")

@app.route("/add_assignment", methods=["GET", "POST"])
def add_assignment():
    # get the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's classes
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    users_classes = []
    for room in classes:
        users_classes.append(room["class"])

    # list of user's assignments
    assignments = db.execute("SELECT name FROM assignments WHERE users_id = ? ORDER BY remaining_time", session["user_id"])
    users_assignment_names = []
    for assignment in assignments:
        users_assignment_names.append(assignment["name"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    if request.method == "POST":
        # if the class for the assignment was not provided or it does not exist
        if not request.form.get("class_of_assignment") or request.form.get("class_of_assignment") not in users_classes:
            flash('Invalid Class for New Assignment', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # if no name for the assignment was provided
        if not request.form.get("assignment_name"):
            flash('Missing Name of Assignment', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # if the assignment already exists
        if request.form.get("assignment_name") in users_assignment_names:
            flash('Assignment Name Already Exists', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # if the type of the assignment was not provided
        if not request.form.get("type"):
            flash('Missing Type of New Assignment', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # if the due date was not provided
        if not request.form.get("date"):
            flash('Missing Due Date for New Assignment', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # if the time the assignment is due is not provided
        if not request.form.get("time"):
            flash('Missing Time for New Assignment', 'danger')
            return render_template("add_assignment.html", name=name, classes=users_classes)

        # gets all of the information about the assignments
        class_of_assignment = request.form.get("class_of_assignment").title()
        assignment = request.form.get("assignment_name")
        type = request.form.get("type")
        date = request.form.get("date")
        link = request.form.get("link")
        time = request.form.get("time")
        subject_for_class = db.execute("SELECT subject FROM subjects_and_classes WHERE class = ? AND users_id = ?", class_of_assignment, session["user_id"])
        subject = subject_for_class[0]["subject"]

        # adds the assignment to the table of assignments
        db.execute("INSERT INTO assignments (users_id, name, type, class, subject, due_date, link, due_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], assignment, type, class_of_assignment, subject, date, link, time)

        # returns a confirmation message
        flash('Assignment Added Successfully', 'success')
        return redirect("/")
    else:
        # displays the page
        return render_template("add_assignment.html", name=name, classes=users_classes)

@app.route("/update_assignment", methods=["GET", "POST"])
def update_assignment():
    # gets the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    # list of user's assignments
    assignments = db.execute("SELECT name FROM assignments WHERE users_id = ? ORDER BY remaining_time", session["user_id"])
    users_assignment_names = []
    for assignment in assignments:
        users_assignment_names.append(assignment["name"])

    # list of user's classes
    users_classes = []
    classes = db.execute("SELECT class FROM subjects_and_classes WHERE users_id = ?", session["user_id"])
    for room in classes:
        users_classes.append(room["class"])

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    if request.method == "POST":
        # if the name of the assignment was not provided or the assignment does not exist
        if not request.form.get("name_of_assignment") or request.form.get("name_of_assignment") not in users_assignment_names:
            flash('Invalid Assignment to Adjust', 'danger')
            return render_template("update_assignment.html", name=name, assignments=users_assignment_names, classes=users_classes)

        # gets all of the information about the assignment
        assignment_row = db.execute("SELECT * FROM assignments WHERE name = ? AND users_id = ?", request.form.get("name_of_assignment"), session["user_id"])
        assignment_id = assignment_row[0]["id"]
        assignment_type = assignment_row[0]["type"]
        assignment_class = assignment_row[0]["class"]

        # if the new name for the assignment is the same as an assignment name (assignment names must be unique)
        if request.form.get("new_assignment_name") in users_assignment_names:
            flash('Assignment Name Must Be Different From the Old One', 'danger')
            return render_template("update_assignment.html", name=name, assignments=users_assignment_names, classes=users_classes)
        else:
            # if the assignment name is valid, then the name is updated
            if request.form.get("new_assignment_name"):
                db.execute("UPDATE assignments SET name = ? WHERE id = ?", request.form.get("new_assignment_name"), assignment_id)

        # if the new class for the assignment is the same as the old one
        if request.form.get("new_assignment_class") == assignment_class:
            flash('Assignment Class Must be Different From the Old One', 'danger')
            return render_template("update_assignment.html", name=name, assignments=users_assignment_names, classes=users_classes)
        else:
            # if a valid class for the assignment was inputted
            if request.form.get("new_assignment_class"):
                subjects = db.execute("SELECT subject FROM subjects_and_classes WHERE class = ?", request.form.get("new_assignment_class"))
                assignment_subject = subjects[0]["subject"]
                db.execute("UPDATE assignments SET class = ?, subject = ? WHERE id = ?", request.form.get("new_assignment_class"), assignment_subject, assignment_id)

        # the type of the assignment is switched (choices are online or paper) if the user requests it
        new_type = ""
        if request.form.get("type_switch") and request.form.get("type_switch") == 'Yes':
            if assignment_type == "Online":
                new_type = "Paper"
            else:
                new_type = "Online"
            db.execute("UPDATE assignments SET type = ? WHERE id = ?", new_type, assignment_id)

        # if a link is provided for the assignent
        if request.form.get("link_switch"):
            db.execute("UPDATE assignments SET link = ? WHERE id = ?", request.form.get("link_switch"), assignment_id)

        # if a new due date is provided for the assignent
        if request.form.get("date_switch"):
            db.execute("UPDATE assignments SET due_date = ? WHERE id = ?", request.form.get("date_switch"), assignment_id)

        # if the assignment is due at a different time
        if request.form.get("time_switch"):
            db.execute("UPDATE assignments SET due_time = ? WHERE id = ?", request.form.get("time_switch"), assignment_id)

        # returns a confirmation message
        flash('Assignment Updated Successfully', 'success')
        return redirect("/")
    else:
        # displays the page
        return render_template("update_assignment.html", name=name, assignments=users_assignment_names, classes=users_classes)

@app.route("/review", methods=["GET", "POST"])
def review():
    # gets the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    if request.method == "POST":
        # if no number rating was inputted or an invalid number was inputted
        if not request.form.get("rating") or float(request.form.get("rating")) < 0 or float(request.form.get("rating")) > 5:
            flash('Invalid Rating. Must be value between 0 and 5, inclusive.', 'danger')
            return render_template("review.html", name=name)


        # gets the date of the reivew
        current_time = datetime.now()
        date_of_review = current_time.date()

        # gets the title of the review
        title = request.form.get("title")
        if not title:
            title = "Review for Trackify"

        # adds the review to the table of reviews
        db.execute("INSERT INTO reviews (users_id, stars, description, name, date_of_review, title) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("rating"), request.form.get("review"), name, date_of_review, title)

        # returns a confirmation message
        flash('Review Successfully Created. If you wish to see all of the reviews, visit the link at the bottom right corner.', 'success')
        return render_template("review.html", name=name)
    else:
        # displays the page
        return render_template("review.html", name=name)

@app.route("/reviews_all", methods=["GET", "POST"])
def reviews_all():
    # gets the user's information
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    name = user[0]["username"]

    db.execute("DELETE FROM assignments WHERE status = ?", 'Submitted')

    # access table of reviews
    reviews = db.execute("SELECT * FROM reviews ORDER BY date_of_review DESC")

    # gets the average star rating of all the reviews
    avg_rating_row = db.execute("SELECT AVG(stars) FROM reviews")
    avg_rating = avg_rating_row[0]["AVG(stars)"]
    avg_rating = round(avg_rating, 2)

    return render_template("reviews_all.html", name=name, reviews=reviews, avg_rating=avg_rating)
