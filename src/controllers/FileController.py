from src.validators import FileValidator
from src.services.FileService import FileService

def upload(file):
    response = FileValidator.validate(file)

    if not response:
        file_service = FileService(file)
        
        return { "message": "file service accessed" }

    return response


