# main.py
import os

from flask import Flask, send_file, request, render_template, url_for
from todo_functions import add_todo, get_todos, update_todo_status, delete_todo

app = Flask(__name__)

@app.route("/")
def index():
    todos = get_todos()
    image_url = url_for('static', filename='images/bin.svg')
    return render_template('index.html', todos=todos, image_url=image_url)
    # return send_file('src/index.html')
    # return send_file('src/index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
  task = request.form['task']
  status = request.form['status']
  add_todo(task, status) # Make sure add_todo accepts status
  return "Todo added successfully!"

@app.route('/update/<int:todo_id>', methods=['POST'])
def update(todo_id):
  update_todo_status(todo_id, 'Completed')
  return 'Todo updated successfully', 200
  
@app.route('/delete/<int:todo_id>', methods=['GET']) 
def delete(todo_id):
    delete_todo(todo_id)  # Call the delete function from todo_functions.py
    return "Todo deleted successfully!"

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()

