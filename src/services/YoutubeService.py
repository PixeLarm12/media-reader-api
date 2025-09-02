import tempfile
import subprocess
import os
import shutil
import requests
import whisper
import yt_dlp

from src.exceptions import AppException
from src.enums import HttpEnum

class YoutubeService:
    def __init__(self, url: str):
        if not url:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] You must provide a valid URL."
            )

        self.url = url
        try:
            self.model = whisper.load_model("base")
        except Exception as e:
            raise AppException(
                code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] Failed to load Whisper model: {str(e)}"
            )

        self._temp_files = [] 
        self._temp_dirs = []

    def _is_youtube(self) -> bool:
        return "youtube.com" in self.url or "youtu.be" in self.url

    def _download_youtube(self) -> str:
        tmp_dir = tempfile.mkdtemp()
        self._temp_dirs.append(tmp_dir)

        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': os.path.join(tmp_dir, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] Failed to download YouTube video: {str(e)}"
            )

        files = os.listdir(tmp_dir)
        if not files:
            raise AppException(
                code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] No files were downloaded from YouTube"
            )

        return os.path.join(tmp_dir, files[0])

    def _download_http(self) -> str:
        try:
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise AppException(
                code=HttpEnum.Code.BAD_REQUEST,
                message=f"[{HttpEnum.Message.BAD_REQUEST.value}] Failed to download file from URL: {str(e)}"
            )

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        with open(tmp_file.name, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        self._temp_files.append(tmp_file.name)
        return tmp_file.name

    def _extract_audio(self, video_path: str) -> str:
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        self._temp_files.append(audio_path)

        process = subprocess.run([
            "ffmpeg", "-i", video_path, "-vn",
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            audio_path, "-y"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            raise AppException(
                code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] FFmpeg failed: {process.stderr.decode('utf-8')}"
            )

        return audio_path

    def transcribe(self) -> str:
        try:
            if self._is_youtube():
                video_path = self._download_youtube()
            else:
                video_path = self._download_http()

            audio_path = self._extract_audio(video_path)

            try:
                result = self.model.transcribe(audio_path)
            except Exception as e:
                raise AppException(
                    code=HttpEnum.Code.INTERNAL_SERVER_ERROR,
                    message=f"[{HttpEnum.Message.INTERNAL_SERVER_ERROR.value}] Whisper transcription failed: {str(e)}"
                )

            return result["text"]

        finally:
            self.cleanup()

    def cleanup(self):
        for f in self._temp_files:
            try:
                if os.path.isfile(f):
                    os.remove(f)
            except Exception:
                pass

        for d in self._temp_dirs:
            try:
                if os.path.isdir(d):
                    shutil.rmtree(d)
            except Exception:
                pass

        self._temp_files.clear()
        self._temp_dirs.clear()
