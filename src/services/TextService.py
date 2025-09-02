from fastapi import UploadFile
from pathlib import Path
from src.enums import HttpEnum
from src.exceptions import AppException

class TextService:
    SUPPORTED_EXTENSIONS = [".txt", ".md"]

    def __init__(self, file: UploadFile):
        self.file = file

    async def transcribe(self):
        try:
            ext = Path(self.file.filename).suffix.lower()
            if ext not in self.SUPPORTED_EXTENSIONS:
                raise AppException(
                    code=HttpEnum.Code.UNPROCESSABLE_ENTITY,
                    message=f"[{HttpEnum.Message.UNPROCESSABLE_ENTITY.value}] Extension {ext} not supported",
                    data=[]
                )

            content_bytes = await self.file.read()
            content_str = content_bytes.decode("utf-8")

            return content_str.strip()
        except Exception as e:
            raise AppException(
                code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] Error transcribing Text: {str(e)}",
                data=[]
            )
