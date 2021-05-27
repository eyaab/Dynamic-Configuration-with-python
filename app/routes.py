from flask import Flask, render_template,  request, jsonify, redirect, url_for
from app import app
from app import database as db_helper


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    # db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


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
