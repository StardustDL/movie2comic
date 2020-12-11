import os
import uuid
import shutil
from . import settings

_ALLOWED_EXTENSIONS = ["mp4", "mpeg", "mpg", "wmv", "mov", "avi"]


def _is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in _ALLOWED_EXTENSIONS


class Session:
    def __init__(self, sid=None, data_root=None):
        if sid is None:
            sid = str(uuid.uuid1())
        if data_root is None:
            data_root = settings.DATA_PATH
        self.id = sid
        self.data_path = os.path.join(data_root, self.id)
        self.input_path = os.path.join(self.data_path, "input.dat")
    
    def exists(self):
        return os.path.exists(self.data_path)

    def initialize(self):
        os.mkdir(self.data_path)

    def input(self, request_file) -> bool:
        if _is_allowed_file(request_file.filename):
            request_file.save(self.input_path)
            return True
        return False

    def clear(self):
        shutil.rmtree(self.data_path)
