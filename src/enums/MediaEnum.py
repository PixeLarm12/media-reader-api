from enum import Enum

class Types(Enum):
    YOUTUBE = 1
    TEXT = 2
    DOC = 3
    AUDIO = 4
    VIDEO = 5

class Extension(Enum):
    # Text
    TXT = ".txt"
    MD = ".md"
    PDF = ".pdf"

    # Audio
    MP3 = ".mp3"
    WAV = ".wav"
    OGG = ".ogg"
    FLAC = ".flac"
    M4A = ".m4a"

    # Video
    MP4 = ".mp4"
    AVI = ".avi"
    MOV = ".mov"
    MKV = ".mkv"

class ContentType(Enum):
    # Text
    TEXT = "text/plain"
    MARKDOWN = "text/markdown"
    PDF = "application/pdf"

    # Audio
    MP3 = "audio/mpeg"
    WAV = "audio/wav"
    OGG = "audio/ogg"
    FLAC = "audio/flac"
    M4A = "audio/mp4"

    # Video
    MP4 = "video/mp4"
    AVI = "video/x-msvideo"
    MOV = "video/quicktime"
    MKV = "video/x-matroska"

TEXT_EXTENSIONS = [Extension.TXT.value, Extension.MD.value]
AUDIO_EXTENSIONS = [Extension.MP3.value, Extension.WAV.value, Extension.OGG.value, Extension.FLAC.value, Extension.M4A.value]
VIDEO_EXTENSIONS = [Extension.MP4.value, Extension.AVI.value, Extension.MOV.value, Extension.MKV.value]
DOC_EXTENSIONS = [Extension.PDF.value]
TYPES_STRING = {
    Types.TEXT.value: "Text",
    Types.DOC.value: "Document",
    Types.AUDIO.value: "Audio",
    Types.VIDEO.value: "Video",
}

ALL_EXTENSIONS = TEXT_EXTENSIONS + AUDIO_EXTENSIONS + VIDEO_EXTENSIONS + DOC_EXTENSIONS