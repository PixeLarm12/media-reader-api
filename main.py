from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.controllers import FileController as file_controller
from src.utils.HttpUtil import HttpUtil
from src.exceptions import AppException
from src.enums import HttpEnum
from enum import Enum

app = FastAPI()

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return HttpUtil.response(
        data=exc.data,
        code=exc.code,
        message=exc.message
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")

    return HttpUtil.response(
        data=[],
        code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
        message=str(exc) or HttpEnum.Message.INTERNAL_SERVER_ERROR
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(media):
    content, code, message = await file_controller.analyze_media(media)
    return HttpUtil.response(content, code, message)