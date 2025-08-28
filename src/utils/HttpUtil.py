from src.enums import HttpEnum

def response(data, code = HttpEnum.Code.OK.value, message = HttpEnum.Message.OK):
    return {
        "code": code,
        "message": message,
        "data": data
    }