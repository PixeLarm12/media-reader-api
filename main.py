from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import FileController as file_controller
from src.utils import HttpUtil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-url")
async def analyzeUrl(url: str):
    content, code, message = file_controller.analyze_url(url)
    return HttpUtil.response(content, code, message)

@app.post("/analyze-text")
async def analyzeText(file: UploadFile):
    content, code, message = await file_controller.analyze_text(file)
    return HttpUtil.response(content, code, message)

@app.post("/analyze-pdf")
async def analyzePdf(file: UploadFile):
    content, code, message = await file_controller.analyze_pdf(file)
    return HttpUtil.response(content, code, message)