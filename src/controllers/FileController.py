from src.validators import FileValidator
from src.services.YoutubeService import YoutubeService
from src.enums import HttpEnum

def analyze(url):
    service = YoutubeService(url)
    text = service.transcribe()
    
    code = HttpEnum.HttpStatusCode.OK
    message = ''

    if not text:
        code = HttpEnum.HttpStatusCode.INTERNAL_SERVER_ERROR
        message = HttpEnum.HttpStatusMessage.INTERNAL_SERVER_ERROR

    return text, code, message
    
