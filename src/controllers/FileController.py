from src.validators import FileValidator
from src.services import YoutubeService, TextService, PdfService, AudioService
from src.enums import HttpEnum

def analyze_url(url):
    service = YoutubeService(url)
    text = service.transcribe()
    
    code = HttpEnum.Code.OK
    message = ''

    if not text:
        code = HttpEnum.Code.INTERNAL_SERVER_ERROR
        message = HttpEnum.Message.INTERNAL_SERVER_ERROR

    return text, code, message

async def analyze_text(file):
    service = TextService(file)
    text = await service.transcribe()
    
    code = HttpEnum.Code.OK
    message = ''

    if not text:
        code = HttpEnum.Code.INTERNAL_SERVER_ERROR
        message = HttpEnum.Message.INTERNAL_SERVER_ERROR

    return text, code, message

async def analyze_pdf(file):
    service = PdfService(file)
    text = await service.transcribe()
    
    code = HttpEnum.Code.OK
    message = ''

    if not text:
        code = HttpEnum.Code.INTERNAL_SERVER_ERROR
        message = HttpEnum.Message.INTERNAL_SERVER_ERROR

    return text, code, message

async def analyze_audio(file):
    service = AudioService(file)
    text = await service.transcribe()
    
    code = HttpEnum.Code.OK
    message = ''

    if not text:
        code = HttpEnum.Code.INTERNAL_SERVER_ERROR
        message = HttpEnum.Message.INTERNAL_SERVER_ERROR

    return text, code, message