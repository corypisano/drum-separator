import os

from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from config import Config
from audio_separator import load_waveform_from_file, save_to_file, separate_from_waveform
from utils.S3_manager import upload_file, create_presigned_url

app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
BUCKET_NAME = 'drum-separator'

@app.route('/health')
def health():
    return 'Hello, World!', 200

@app.route('/upload', methods=['POST'])
def upload():
    if request.method != 'POST':
        return "invalid request", 400
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash(f"Allowed file types are {list(ALLOWED_EXTENSIONS)}")
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    print(f"file.filename={file.filename}, filename={filename}")
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(f"./uploads/{filename}")
    flash('File successfully uploaded')
    return redirect(url_for('process_file', filename=filename))

@app.route('/process_file')
def process_file():
    filename = request.args['filename']
    print(f"in process_file, received filename = {filename}")
    #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filepath = f"./uploads/{filename}"

    # load raw waveform from input file
    print(f"now loading wabeform with filepath = {filepath}")
    waveform, sample_rate = load_waveform_from_file(filepath)

    # perform audio separation
    print('now separating waveform')
    result = separate_from_waveform(waveform)

    out_file = f'./tmp_out/drums_{filename}'
    result_file = save_to_file(result['drums'], out_file, sample_rate)

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