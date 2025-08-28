from fastapi import UploadFile
from pathlib import Path
from src.enums import HttpEnum

class TextService:
    SUPPORTED_EXTENSIONS = [".txt", ".md"]

    def __init__(self, file: UploadFile):
        self.file = file

    async def transcribe(self):
        try:
            ext = Path(self.file.filename).suffix.lower()
            if ext not in self.SUPPORTED_EXTENSIONS:
                return {
                    "content": None,
                    "code": HttpEnum.Code.UNSUPPORTED_MEDIA.value,
                    "message": HttpEnum.Message.UNSUPPORTED_MEDIA.value
                }

            content_bytes = await self.file.read()
            content_str = content_bytes.decode("utf-8")

            transcript = content_str.strip()

            return {
                "content": transcript,
                "code": HttpEnum.Code.OK.value,
                "message": HttpEnum.Message.OK.value
            }

        except Exception as e:
            return {
                "content": None,
                "code": HttpEnum.Code.INTERNAL_SERVER_ERROR.value,
                "message": f"{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}: {str(e)}"
            }
