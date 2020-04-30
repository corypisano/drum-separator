from flask import render_template, Blueprint, jsonify, request, current_app

from app.audio_separator import separate_drums
from app.constants import ALLOWED_EXTENSIONS
from app.file_manager import save_file

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def home():
    return render_template("home.html")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/upload', methods=['POST'])
def upload():
    print('in upload')
    if 'file' not in request.files:
        return "no file yo", 404
    f = request.files['file']
    print('filename')
    print(f.filename)
    if not allowed_file(f.filename):
        return "nah, file not allowed", 400
    
    filename = secure_filename(f.filename)
    filepath = f"./tmp/{filename}"
    f.save(filepath)
    message = filename
    return message, 200

@api.route("/process", methods=["POST"])
def process():
    print(f"in POST /process")
    if 'file' not in request.files:
        return "no file yo", 404
    f = request.files['file']
    if not allowed_file(f.filename):
        return "nah, file not allowed", 400
    print("saving file")
    filepath = save_file(f)

    print('now separating waveform')
    output_dir = './tmp_out'
    separate_drums(filepath, output_dir)
    print('done')
    response = {
        "success": True,
        "drum_link": "https://drum.com",
        "audio_link": "https://audio.com",
    }
    return jsonify(response), 200

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