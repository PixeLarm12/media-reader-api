import os
import tempfile
import subprocess
import speech_recognition as sr

class VideoService:
    SUPPORTED_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv"]

    def __init__(self, file):
        self.file = file

    async def transcribe(self):
        try:
            suffix = os.path.splitext(self.file.filename)[-1].lower()

            if suffix not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Extensão {suffix} não suportada!")

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_video:
                tmp_video.write(await self.file.read())
                tmp_video_path = tmp_video.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio_path = tmp_audio.name

            proc = subprocess.run(
                [
                    "ffmpeg", "-i", tmp_video_path, "-vn",
                    "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                    tmp_audio_path, "-y"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if proc.returncode != 0:
                raise RuntimeError(f"Erro ao extrair áudio: {proc.stderr.decode('utf-8', errors='ignore')}")

            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_audio_path) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data, language="pt-BR")

            os.remove(tmp_video_path)
            os.remove(tmp_audio_path)

            return text

        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise RuntimeError(f"Erro ao se conectar ao serviço de reconhecimento: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro na transcrição do vídeo: {e}")
