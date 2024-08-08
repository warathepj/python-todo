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
