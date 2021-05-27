from flask import Flask, render_template,  request, jsonify, redirect, url_for
from app import app
from app import database as db_helper
import sqlite3 as sql

# connect to tasks_database.sq (database will be created, if not exist)
con = sql.connect('tasks_database.db')
con.execute('CREATE TABLE IF NOT EXISTS tbl_tasks (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'task TEXT, status TEXT)')
con.close

@app.route("/create", methods=['GET', 'POST'])
def create():
     if request.method == 'GET':
            # send the form
            return render_template('index.html')
     else:
     # request.method == 'POST':
     # read data from the form and save in variable
            task = request.form['task']
            status = 'todo'
            # store in database
            try:
                con = sql.connect('tasks_database.db')
                c =  con.cursor() # cursor
                # insert data
                c.execute("INSERT INTO tbl_tasks (task, status) VALUES (?,?)",
                (task, status))
                con.commit() # apply changes
                # go to thanks page
                return render_template('index.html', task=task)
            except con.Error as err: # if error
                # then display the error in 'database_error.html' page
                return render_template('database_error.html', error=err)
            finally:
                con.close() # close the connection



@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    data = request.get_json()
    print(data)
    try:
        if "status" in data:
            # db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            # db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):

    try:
        # db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/")
def homepage():
    # @TO DO bring items from BD
    items = [
        {"id": 1, "task": "Understand dynamic config management", "status": "Complete"},
        {"id": 2, "task": "Search papers related to dynamic config management",
            "status": "In Progress"},
        {"id": 3, "task": "Arrange a meetings with our mentor",
                          "status": "In Progress"},
    ]
    return render_template("index.html", items=items)
