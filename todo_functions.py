# todo_functions.py
# from todo_functions.py, how to create ui for input task and status.


#######
import random
import string
import sqlite3


def get_data(user):

    # for debug
    # def get_data():
    conn = sqlite3.connect(
        "todo.db"
    )  # Replace 'your_database.db' with your actual database file
    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    cursor.execute("SELECT * FROM todos WHERE user = ?", (user,))

    # cursor.execute(
    #     "SELECT * FROM todos WHERE user = '4'"
    # )  # Replace 'your_table' with your actual table name
    data = cursor.fetchall()

    conn.close()
    return data


# for debug


# from main.py, how to create new python file for
def add_todo(task, status, user):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO todos(task, status, user) VALUES(?,?,?)""", (task, status, user)
    )
    conn.commit()
    conn.close()


def get_todos():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM todos""")
    # todos_from_db = cursor.fetchall()
    todos = cursor.fetchall()
    conn.close()
    # return todos_from_db
    return todos


def get_todo(todo_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id=?", (todo_id,))
    todo = cursor.fetchone()
    conn.close()
    return todo


# create def update_todo in todo_functions.py, reference main.py, templates/index.html
def update_todo(todo_id, task, status):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE todos SET task = ?, status = ? WHERE id = ?""",
        (task, status, todo_id),
    )
    conn.commit()
    conn.close()


def update_todo_status(todo_id, new_status):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    # cursor.execute('''UPDATE todos SET status = ? WHERE id = ?''', (status, todo_id))
    cursor.execute(
        """UPDATE todos SET status = ? WHERE id = ?""", (new_status, todo_id)
    )
    conn.commit()
    conn.close()


def delete_todo(todo_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()


# Generate a random letter from a to z
uname = random.choice(string.ascii_lowercase)

print(uname)  # Output the generated letter
