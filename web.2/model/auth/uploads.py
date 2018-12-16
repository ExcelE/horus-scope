from .common import *
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import send_from_directory

class Uploads(Resource):
    def get(self, filename):

        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
