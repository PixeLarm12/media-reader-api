from src.enums import FileEnum
from src.utils import FileUtil

def validate(file):
    content_type = file.content_type
    file_extension = FileUtil.getFileExtension(file)
    
    return False