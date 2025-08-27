from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import FileController as file_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping_pong():
    return { "pong" }

@app.post("/upload")
async def upload(file: UploadFile):
    return { "success": file_controller.upload(file) }    