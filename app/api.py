import redis
from rq import Queue, Connection
from flask import render_template, Blueprint, jsonify, request, current_app

from app.worker import create_task

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@api.route("/tasks", methods=["POST"])
def run_task():
    print('POST /tasks')
    task_type = request.form["type"]
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(create_task, task_type)
        print('task = ', task)
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


@api.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)