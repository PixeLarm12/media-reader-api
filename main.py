from fastapi import FastAPI
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

@app.post("/analyze")
async def analyze(url):
    content, code, message = file_controller.analyze(url)
    return HttpUtil.response(content, code, message)