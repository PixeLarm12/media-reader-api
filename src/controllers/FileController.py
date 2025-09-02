from src.validators import FileValidator
from src.services import YoutubeService, TextService, PdfService, AudioService, VideoService
from src.enums import HttpEnum
from src.exceptions import AppException

def analyze_youtube(url):
    service = YoutubeService(url)
    text = service.transcribe()
    
    if not text:
        raise AppException(
            code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message = HttpEnum.Message.INTERNAL_SERVER_ERROR
        )

    return text, HttpEnum.Code.OK, ''

async def analyze_video(file):
    service = VideoService(file)
    text = await service.transcribe()
    
    if not text:
        raise AppException(
            code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message = HttpEnum.Message.INTERNAL_SERVER_ERROR
        )

    return text, HttpEnum.Code.OK, ''

async def analyze_text(file):
    service = TextService(file)
    text = await service.transcribe()
    
    if not text:
        raise AppException(
            code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message = HttpEnum.Message.INTERNAL_SERVER_ERROR
        )

    return text, HttpEnum.Code.OK, ''

async def analyze_pdf(file):
    service = PdfService(file)
    text = await service.transcribe()
    
    if not text:
        raise AppException(
            code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message = HttpEnum.Message.INTERNAL_SERVER_ERROR
        )

    return text, HttpEnum.Code.OK, ''

async def analyze_audio(file):
    service = AudioService(file)
    text = await service.transcribe()
    
    if not text:
        raise AppException(
            code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message = HttpEnum.Message.INTERNAL_SERVER_ERROR
        )

    return text, HttpEnum.Code.OK, ''