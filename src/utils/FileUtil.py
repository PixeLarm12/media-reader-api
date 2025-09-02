import os
from src.exceptions import AppException
from src.enums import HttpEnum, MediaEnum

def getFileExtension(file):
    _, extension = os.path.splitext(file.filename)
    return extension

def getFileName(file):
    filename, _ = os.path.splitext(file.filename)
    return filename

def redirectByFileType(file):
    extension = getFileExtension(file)
    redirect = 'midi'

    if extension == '.mp3':
        redirect = 'transcribe'

    return redirect

def validate_extension(media_extension: str, allowed_extensions: list, media_type: int):
    media_type_string = MediaEnum.TYPES_STRING[media_type]

    if media_extension not in allowed_extensions:
        raise AppException(
            code=HttpEnum.Code.UNPROCESSABLE_ENTITY,
            message=f"[{HttpEnum.Message.UNPROCESSABLE_ENTITY.value}] The media type '{media_type_string}' does not support extension '{media_extension}'.",
            data=[]
        )