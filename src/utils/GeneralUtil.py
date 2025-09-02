from src.services import TextService, PdfService, AudioService, VideoService
from src.enums import MediaEnum

def map_media_services(type: int):
    mapping = {
        MediaEnum.Types.TEXT.value: (TextService, MediaEnum.TEXT_EXTENSIONS),
        MediaEnum.Types.DOC.value: (PdfService, MediaEnum.DOC_EXTENSIONS),
        MediaEnum.Types.AUDIO.value: (AudioService, MediaEnum.AUDIO_EXTENSIONS),
        MediaEnum.Types.VIDEO.value: (VideoService, MediaEnum.VIDEO_EXTENSIONS),
    }

    return mapping.get(type)
