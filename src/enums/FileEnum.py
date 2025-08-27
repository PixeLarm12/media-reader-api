from enum import Enum

class ContentTypes(Enum):
    # Text
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    TEXT_CSV = "text/csv"
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"

    # Audio
    AUDIO_MP3 = "audio/mpeg"
    AUDIO_WAV = "audio/wav"

    # Video
    VIDEO_MP4 = "video/mp4"
    VIDEO_WEBM = "video/webm"


class Extensions(Enum):
    # Text
    TXT = ".txt"
    HTML = ".html"
    CSV = ".csv"
    JSON = ".json"
    XML = ".xml"

    # Audio
    MP3 = ".mp3"
    WAV = ".wav"

    # Video
    MP4 = ".mp4"
    WEBM = ".webm"
    AVI = ".avi"
    MOV = ".mov"
