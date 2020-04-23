import os

from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from celery import Celery

from config import Config
from audio_separator import separate_drums
from S3_manager import upload_file, create_presigned_url

app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
BUCKET_NAME = 'drum-separator'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def hello():
    return "Hello, 200"

@app.route('/health')
def health():
    return "ok", 200

@celery.task(bind=True)
def my_background_task(arg1, arg2):
    # some long running task here
    self.update_state(state='STARTED')
    
    self.update_state(state='DONE')
    return result

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = my_background_task.AsyncResult(task_id)
    return {'state': task.state}, 200

@app.route('/task')
def run_task():
    task = my_background_task.apply_async(args=[10, 20])
    return {'task_id': task.id}, 200

@app.route('/upload', methods=['POST'])
def upload():
    if request.method != 'POST':
        return "invalid request", 400
    data = request.form.to_dict(flat=False)
    print('data = ', data)
    print('json')
    print(request.get_json())
    data2 = request.get_data()
    print('data2 = ', data2)
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return "no file yo", 404
    f = request.files['file']
    print('filename')
    print(f.filename)
    if not allowed_file(f.filename):
        print(f"Allowed file types are {list(ALLOWED_EXTENSIONS)}")
        return "nah, file not allowed", 400
    
    filename = secure_filename(f.filename)
    print(f"file.filename={f.filename}, filename={filename}")
    f.save(f"./uploads/{filename}")
    message = filename
    return message, 200

@app.route('/separate')
def separate():
    input_file = ''
    output_dir = ''
    separate_drums(input_file, output_dir)

@app.route('/process_file')
def process_file():
    filename = request.args['filename']
    print(f"in process_file, received filename = {filename}")
    filepath = f"./uploads/{filename}"

    # save file to local filesystem

    # perform audio separation
    print('now separating waveform')
    input_file = 'NewYorican.mp3'
    output_dir = './tmp_out'
    result = separate_drums(input_file, output_dir)

    # upload result drum file to s3
    s3_key = f'drums_s3_{filename}'
    upload_file(out_file, bucket=BUCKET_NAME, object_name=s3_key)

    # create_presigned_url(bucket, obj name, expiration)
    drum_url = create_presigned_url(BUCKET_NAME, s3_key)

    print(f'drum_url = {drum_url}')
    return f'<h3>Drum only track</h3><a href={drum_url}>{drum_url}</a'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run()