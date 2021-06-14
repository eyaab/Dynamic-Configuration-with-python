from flask import Flask, config, render_template,  request, jsonify, redirect, url_for
from app import app, configuration
import sqlite3 as sql
from flask_apscheduler import APScheduler

# connect to tasks_database.sq (database will be created, if not exist)
con = sql.connect('tasks_database.db')
con.execute('CREATE TABLE IF NOT EXISTS tbl_tasks (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'task TEXT, status TEXT)')
con.close()

scheduler = APScheduler()
scheduler.add_job(func=configuration.update,
                  trigger='interval', id='job', seconds=1)
scheduler.start()


@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # send the form
        return render_template('index.html')
    else:
        # request.method == 'POST':
        # read data from the form and save in variable
        task = request.get_json()['task']
        status = 'Todo'
        # store in database
        try:
            con = sql.connect('tasks_database.db')
            c = con.cursor()  # cursor
            # insert data
            c.execute("INSERT INTO tbl_tasks (task, status) VALUES (?,?)",  # fix sql injection
                      (task, status))
            con.commit()  # apply changes
            # go to thanks page
            return render_template('index.html', task=task)
        except con.Error as err:  # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            con.close()  # close the connection


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    status = request.get_json()['status']
    try:
        con = sql.connect('tasks_database.db')
        cur = con.cursor()
        query = "UPDATE tbl_tasks SET status='{}' WHERE ID={}".format(  # fix sql injection
            status, task_id)
        print(query)
        cur.execute(query)
        con.commit()
        result = {'success': True, 'response': 'Status Updated'}
    except sql.Error as error:
        print("Failed to update sqlite table", error)
        result = {'success': False, 'response': 'Something went wrong'}
    finally:
        con.close()  # close the connection
    return jsonify(result)


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):

    try:
        con = sql.connect('tasks_database.db')
        cur = con.cursor()
        query = 'DELETE FROM tbl_tasks WHERE ID={}'.format(
            task_id)  # fix sql injection
        cur.execute(query)
        con.commit()
        con.close()
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/")
def homepage():
    con = sql.connect('tasks_database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl_tasks")

    rows = cur.fetchall()
    items = []
    for row in rows:
        items.append({'id': row[0], 'task': row[1], 'status': row[2]})

    # @TO DO bring items from BD

    print(configuration.config["backgroundColor"])
    backgroundColor = configuration.config["backgroundColor"]
    # in another process
    #c.kv.put('foo', 'bar')

    return render_template("index.html", items=items, backgroundColor=backgroundColor)
