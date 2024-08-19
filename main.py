# main.py
# from main.py, all route redirect to /login
# from main.py, make route to /login
#from /add add button for go to /, reference main.py
import os

from flask import Flask, send_file, request, render_template, url_for, flash, redirect, jsonify
# from todo_functions import add_todo, get_todos, get_todo, update_todo, update_todo_status, delete_todo
from todo_functions import *

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/")
def index():
    todos = get_todos()
    image_url = url_for('static', filename='images/bin.svg')
    image_url1 = url_for('static', filename='images/edit.svg')
    return render_template('index.html', todos=todos, image_url=image_url, image_url1=image_url1)
    # return send_file('src/index.html')
    # return send_file('src/index.html', todos=todos)

@app.route('/db')
def display_db():
    conn = sqlite3.connect('todo.db')  # Connect to the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")  # Execute a SELECT query
    data = cursor.fetchall()  # Fetch all the data
    conn.close()  # Close the connection
    return render_template('db.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    status = request.form.get('status')
    add_todo(task, status)
    return render_template('add.html')


# @app.route('/update/<int:todo_id>', methods=['POST'])
# def update(todo_id):
#   update_todo_status(todo_id, 'Completed')
#   return 'Todo updated successfully', 200

@app.route('/edit/<todo_id>')
def edit(todo_id):
    todo = get_todo(todo_id)  # Assuming you have a get_todo function in todo_functions.py
    return render_template('edit.html', todo=todo)

@app.route('/update/<todo_id>', methods=['POST'])
def update(todo_id):
    task = request.form['task']
    status = request.form['status']
    update_todo(todo_id, task, status)  # Assuming you have an update_todo function in todo_functions.py
    # update_todo_status(todo_id, 'Completed')  # Assuming you have this function in todo_functions.py

    
    return redirect('/')

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    todo_id = data['id']
    new_status = data['status']
    
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, todo_id))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})


@app.route('/delete/<int:todo_id>', methods=['GET']) 
def delete(todo_id):
    delete_todo(todo_id)  # Call the delete function from todo_functions.py
#in main.py, after
    return render_template('delete_success.html')
    # .5sec redirect('/')

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()

