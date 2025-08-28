from PyPDF2 import PdfReader
from pathlib import Path
import re

class PdfService:
    SUPPORTED_EXTENSIONS = ['.pdf']

    def __init__(self, file):
        self.file = file
        self.extension = Path(file.filename).suffix.lower()

    def validate(self):
        if self.extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Extensão {self.extension} não suportada pelo PdfService")

    async def transcribe(self):
        self.validate()
        try:
            reader = PdfReader(self.file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
        except Exception as e:
            raise RuntimeError(f"Erro ao transcrever PDF: {str(e)}")
