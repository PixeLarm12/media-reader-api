from PyPDF2 import PdfReader
from pathlib import Path
from src.enums import HttpEnum
from src.exceptions import AppException
import re

class PdfService:
    SUPPORTED_EXTENSIONS = ['.pdf']

    def __init__(self, file):
        self.file = file
        self.extension = Path(file.filename).suffix.lower()

    def validate(self):
        if self.extension not in self.SUPPORTED_EXTENSIONS:
            raise AppException(
                code=HttpEnum.Code.UNPROCESSABLE_ENTITY,
                message=f"[{HttpEnum.Message.UNPROCESSABLE_ENTITY.value}] Extension {self.extension} not supported.",
                data=[]
            )

    async def transcribe(self):
        self.validate()
        try:
            reader = PdfReader(self.file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
        except Exception as e:
            raise AppException(
                code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] Error transcribing PDF: {str(e)}",
                data=[]
            )
