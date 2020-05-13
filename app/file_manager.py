from werkzeug.utils import secure_filename


def save_file(input_file):
    """Saves file to tmp directory"""
    filename = secure_filename(input_file.filename)
    filepath = f"./tmp/{filename}"
    input_file.save(filepath)
    return filepath
