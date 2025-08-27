import tempfile
from io import BytesIO

class FileService:
    def __init__(self, file=None):
        if file:
            self._media_file = BytesIO(file.file.read())
        else:
            raise ValueError("You must provide either a file.")

    @property
    def media_file(self):
        return self._media_file

    @media_file.setter
    def media_file(self, value):
        self._media_file = BytesIO(value.file.read())

