# todo_functions.py
#from todo_functions.py, how to create ui for input task and status.

import sqlite3

#from main.py, how to create new python file for
def add_todo(task, status):
  conn = sqlite3.connect('todo.db')
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO todos(task, status) VALUES(?,?)''', (task, status))
  conn.commit()
  conn.close()

def get_todos():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM todos''')
    todos = cursor.fetchall()
    conn.close()
    return todos

def get_todo(todo_id):
       conn = sqlite3.connect('todo.db')
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM todos WHERE id=?", (todo_id,))
       todo = cursor.fetchone()
       conn.close()
       return todo

# create def update_todo in todo_functions.py, reference main.py, templates/index.html
def update_todo(todo_id, task, status):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE todos SET task = ?, status = ? WHERE id = ?''', (task, status, todo_id))
    conn.commit()
    conn.close()

def update_todo_status(todo_id, status):
  conn = sqlite3.connect('todo.db')
  cursor = conn.cursor()
  cursor.execute('''UPDATE todos SET status = ? WHERE id = ?''', (status, todo_id))
  conn.commit()
  conn.close()

def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,)) 
    conn.commit()
    conn.close()
