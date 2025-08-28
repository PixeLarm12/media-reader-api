import tempfile
import subprocess
import os
import shutil
import requests
import whisper
import yt_dlp

class YoutubeService:
    def __init__(self, url: str):
        if not url:
            raise ValueError("You must provide a URL.")
        self.url = url
        self.model = whisper.load_model("base")
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

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        files = os.listdir(tmp_dir)
        if not files:
            raise RuntimeError("There's an error downloading YouTube video")

        video_path = os.path.join(tmp_dir, files[0])
        return video_path

    def _download_http(self) -> str:
        response = requests.get(self.url, stream=True)
        response.raise_for_status()

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
            raise RuntimeError(f"FFmpeg failed: {process.stderr.decode('utf-8')}")

        return audio_path

    def transcribe(self) -> str:
        try:
            if self._is_youtube():
                video_path = self._download_youtube()
            else:
                video_path = self._download_http()

            audio_path = self._extract_audio(video_path)
            result = self.model.transcribe(audio_path)
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
