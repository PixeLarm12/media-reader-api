from fastapi import UploadFile
from src.validators import FileValidator
from src.services import YoutubeService, TextService, PdfService, AudioService, VideoService
from src.enums import HttpEnum, MediaEnum
from src.exceptions import AppException
from src.utils import FileUtil

async def analyze_media(media):
    content = []
    code = HttpEnum.Code.INTERNAL_SERVER_ERROR,
    message = f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] Some error occured with the media uploaded."

    if isinstance(media, str):
        service = YoutubeService(media)
        content = service.transcribe()
    if isinstance(media, UploadFile):
        media_extension = FileUtil.getFileExtension(UploadFile)

        if media_extension in  MediaEnum.TEXT_EXTENSIONS:
            service = TextService(media)
            content = await service.transcribe()
        elif media_extension in  MediaEnum.VIDEO_EXTENSIONS:
            service = VideoService(media)
            content = await service.transcribe()
        elif media_extension in  MediaEnum.AUDIO_EXTENSIONS:
            service = AudioService(media)
            content = await service.transcribe()
        elif media_extension in  MediaEnum.DOC_EXTENSIONS:
            service = PdfService(media)
            content = await service.transcribe()
        else:
            content = []
            code = HttpEnum.Code.BAD_REQUEST
            message = f"[{HttpEnum.Message.BAD_REQUEST.value}] The media type is not supported. Extension {media_extension}"

    if not content:
        raise AppException(
            code,
            message
        )

    return content, HttpEnum.Code.OK, ''