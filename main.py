# main.py

import os

from flask import (
    Flask,
    send_file,
    request,
    render_template,
    url_for,
    redirect,
    jsonify,
    session,
    flash,
)
from functools import wraps
from todo_functions import *

app = Flask(__name__)
app.secret_key = "anl88"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # Get the max user number and set new_user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(CAST(user AS INTEGER)) FROM todos")
    max_number = cursor.fetchone()[0]
    new_user = max_number + 1 if max_number is not None else 1
    print(type(new_user))  # int
    conn.close()

    username = request.form["username"]
    if username == "user":
        session["logged_in"] = True

        # Set new_user in the session
        session["new_user"] = new_user

        flash("Login successful", "success")
        return redirect(url_for("index"))
    else:
        flash("Invalid username", "danger")
        return redirect(url_for("login_page"))


@app.route("/")
@login_required
def index():
    print(session)  # Check if 'logged_in' is in the session
    # todos_from_db = get_todos()  # Make sure this function is defined

    # data = get_data()
    # todos = get_todos()  # Make sure this function is defined
    image_url = url_for("static", filename="images/bin.svg")
    image_url1 = url_for("static", filename="images/edit.svg")
    # Get the new user from the session
    new_user = session.get("new_user", None)
    # new_user = session.get(
    #     "new_user", "N/A"
    # )  # Get new_user from session, default to "N/A" if not set
    # Filter todos based on new_user
    # filtered_todos = [
    #     todo for todo in todos_from_db if todo[3] == new_user
    # ]  # Access user ID
    # Pass new_user to get_data
    data = get_data(new_user)

    # Get the row count
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM todos")
    row_count = cursor.fetchone()[0]
    conn.close()

    return render_template(
        "index.html",
        data=get_data(new_user),
        # todos=filtered_todos,
        # todos=todos,
        image_url=image_url,
        image_url1=image_url1,
        new_user=new_user,
        row_count=row_count,  # Pass the row count to the template
    )


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("new_user", None)  # Clear new_user from session
    return redirect(url_for("login_page"))


@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("login_page"))


@app.route("/db")
@login_required
def display_db():
    conn = sqlite3.connect("todo.db")  # Connect to the database
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")  # Execute a SELECT query
    rows = cursor.fetchall()  # Fetch all the data

    # Get column names
    column_names = [description[0] for description in cursor.description]

    conn.close()  # Close the connection
    return render_template("db.html", data=rows, columns=column_names)


def get_first_row_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM todos ORDER BY id ASC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


@app.route("/add", methods=["POST"])
@login_required
def add():
    new_user = session.get("new_user", None)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check the total row count
    cursor.execute("SELECT COUNT(*) FROM todos")
    total_row_count = cursor.fetchone()[0]

    # If row count exceeds 500, delete the first row
    if total_row_count > 500:
        cursor.execute("DELETE FROM todos WHERE id = (SELECT MIN(id) FROM todos)")
        conn.commit()

    # Check if the user already has 3 rows
    cursor.execute("SELECT COUNT(*) FROM todos WHERE user = ?", (new_user,))
    user_row_count = cursor.fetchone()[0]
    if user_row_count >= 20:
        conn.close()
        return redirect(url_for("limit_page"))

    # Add the new todo
    task = request.form["task"]
    status = request.form.get("status")
    user = new_user
    add_todo(task, status, user)

    conn.close()
    return render_template("add.html")


@app.route("/limit")
@login_required
def limit_page():
    return render_template("limit.html")


@app.route("/edit/<todo_id>")
@login_required
def edit(todo_id):
    todo = get_todo(
        todo_id
    )  # Assuming you have a get_todo function in todo_functions.py
    return render_template("edit.html", todo=todo)


@app.route("/update/<todo_id>", methods=["POST"])
@login_required
def update(todo_id):
    task = request.form["task"]
    status = request.form["status"]
    update_todo(
        todo_id, task, status
    )  # Assuming you have an update_todo function in todo_functions.py

    return redirect("/")


@app.route("/update_status", methods=["POST"])
@login_required
def update_status():
    data = request.json
    todo_id = data["id"]
    new_status = data["status"]

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, todo_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})


@app.route("/delete/<int:todo_id>", methods=["GET"])
@login_required
def delete(todo_id):
    delete_todo(todo_id)  # Call the delete function from todo_functions.py
    return render_template("delete_success.html")


def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/max_user_number")
def max_user_number():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("SELECT MAX(CAST(user AS INTEGER)) FROM todos")

    # Fetch the result
    max_number = cursor.fetchone()[0]

    new_user = max_number + 1

    conn.close()

    return f"The maximum number in the 'user' column is: {max_number}, and the next available number is: {new_user}"


@app.route("/count_rows")
def count_rows():
    """Counts the number of rows in a specific table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Replace 'your_table_name' with the actual table name
    cursor.execute("SELECT COUNT(*) FROM todos")
    row_count = cursor.fetchone()[0]

    # Return the row count as JSON
    return jsonify({"row_count": row_count})


def main():
    app.run(port=int(os.environ.get("PORT", 80)))


if __name__ == "__main__":
    main()
