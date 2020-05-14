ALLOWED_EXTENSIONS = set(["wav", "mp3"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
