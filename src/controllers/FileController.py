from src.validators import FileValidator
from src.services.FileService import FileService

def upload(file):
    response = FileValidator.validate(file)

    if not response:
        file_service = FileService(file)
        
        return { "message": "file service accessed" }

    return response

def analyze():
    url = "https://www.youtube.com/watch?v=JBClc5YiQII"

    service = FileService(url)
    text = service.transcribe()
    print("Transcrição:", text)


    # url = "https://www.youtube.com/shorts/yUy-tqloVmo"
    
