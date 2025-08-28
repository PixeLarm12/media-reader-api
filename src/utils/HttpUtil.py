from src.enums import HttpEnum

def response(data, code = HttpEnum.HttpStatusCode.OK.value, message = HttpEnum.HttpStatusMessage.OK):
    return {
        "code": code,
        "message": message,
        "data": data
    }