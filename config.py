import os



class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess_password'

    ALLOWED_EXTENSIONS = [
        "gcode"
    ]

    UPLOAD_FOLDER = "files"