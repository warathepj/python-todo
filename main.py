# main.py

import os

from flask import Flask, send_file, request, render_template, url_for, redirect, jsonify, session, flash
from functools import wraps
from todo_functions import *

app = Flask(__name__)
app.secret_key = 'anl88'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if username == 'a':
        session['logged_in'] = True
        flash('Login successful', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username', 'danger')
        return redirect(url_for('login_page'))

@app.route("/")
@login_required
def index():
    print(session)  # Check if 'logged_in' is in the session
    todos = get_todos()  # Make sure this function is defined
    image_url = url_for('static', filename='images/bin.svg')
    image_url1 = url_for('static', filename='images/edit.svg')
    return render_template('index.html', todos=todos, image_url=image_url, image_url1=image_url1)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('login_page'))


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

@app.route('/edit/<todo_id>')
def edit(todo_id):
    todo = get_todo(todo_id)  # Assuming you have a get_todo function in todo_functions.py
    return render_template('edit.html', todo=todo)

@app.route('/update/<todo_id>', methods=['POST'])
def update(todo_id):
    task = request.form['task']
    status = request.form['status']
    update_todo(todo_id, task, status)  # Assuming you have an update_todo function in todo_functions.py
    
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
    return render_template('delete_success.html')

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()

