from fastapi import UploadFile
from src.services import YoutubeService
from src.enums import HttpEnum, MediaEnum
from src.exceptions import AppException
from src.utils import FileUtil, GeneralUtil

async def analyze_media(type: int, path: str = None, media: UploadFile = None):
    if type == MediaEnum.Types.YOUTUBE.value:
        if not path:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] YouTube URL is empty.",
                data=[]
            )
        service = YoutubeService(path)
        content = service.transcribe()
    else:
        if not media:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] Media file is required.",
                data=[]
            )

        media_extension = FileUtil.getFileExtension(media)

        ServiceClass, allowed_extensions = GeneralUtil.map_media_services(type)

        if not ServiceClass:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] The media type {type} is not supported.",
                data=[]
            )

        FileUtil.validate_extension(media_extension, allowed_extensions, type)

        service = ServiceClass(media)
        content = await service.transcribe()

    if not content:
        raise AppException(
            code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
            message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] No content could be extracted from the media.",
            data=[]
        )

    return content, HttpEnum.Code.OK, ''
