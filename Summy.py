from pytube import YouTube
import ollama
import whisper
from email.message import EmailMessage
import ssl
import smtplib
import os
from print_color import print
import queue
import torch
import re
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play


class Summy:
    def __init__(self) -> None:
        # Audio download path
        self.AUDIO_PATH = "media/temp/video_audio.mp3"
        self.TRANSCRIPTION_PATH = "media/temp/transcription.bin"
        self.SUMMARY_PATH = "media/temp/summary.bin"
        # Mail variables
        self.subject = "Resumo do video"
        self.from_email = os.getenv('EMAIL')
        self.from_email_password = os.getenv('EMAIL_PASSWORD')
        # Threads variables
        self.phrase_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.summary = ""

    def get_yt_audio(self, url: str) -> None:
        print("Downloading audio...")
        audio = YouTube(url).streams.filter(only_audio=True).first()
        audio.download(filename=self.AUDIO_PATH)
        print("Audio download done.", color='green')

    def transcribe_audio(self, model: str = "base") -> str:
        print("Transcribing audio...")
        model = whisper.load_model(model)
        result = model.transcribe(self.AUDIO_PATH)
        print("Transcription done.", color='green')

        text = result["text"]
        self.save_text(text, self.TRANSCRIPTION_PATH)

        return text

    def send_email(self, text: str, to_email: str):
        body = text
        em = EmailMessage()

        em['From'] = self.from_email
        em['To'] = to_email
        em['Subject'] = self.subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.from_email, self.from_email_password)
            smtp.sendmail(self.from_email, to_email, em.as_string())
        print("Email sent!", color='green')

    def resume(self, text: str,
               max_caracteres: int = 500) -> str:

        print("Asking LLama3 to resume...")
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': f'Resuma e explique a seguinte transcrição de um video em pt-br. Escreva no máximo {max_caracteres} caracteres. Não use caracter especial pois sua resposta sera passada para um modelo de text-to-speak. Não Dê opniões proprias, apenas explique o texto',
            },
            {
                'role': 'user',
                'content': f"""{text}""",
            }],
            stream=True)

        full_text = ""
        phrase = ""
        for chunk in response:
            phrase += chunk['message']['content']
            if phrase.endswith('.'):
                print(phrase)
                # self.text_to_speak(phrase)
                full_text += phrase
                phrase = ""

        print('Summary done.', color='green')

        self.save_text(full_text, self.SUMMARY_PATH)
        return full_text

    def text_to_speak(self,
                      text: str,
                      voice: str = "./media/voices/female_01.wav",
                      voice_speed: float = "2", language: str = "pt", auto_play: bool = True) -> None:
        print('Dubling...')
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # print("Using: " + device, color="yellow")

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        output_path = "media/output.wav"

        print(f"Voice selected: {voice}", color="blue")
        cleaned_text = re.sub(r'\.', ' ', text)
        tts.tts_to_file(text=cleaned_text,
                        speaker_wav=voice,
                        language=language,
                        file_path=output_path,
                        speed=voice_speed)

        sound = AudioSegment.from_wav(output_path)

        if auto_play:
            play(sound)

        print('Dubling done.', color="green")

    def save_text(self, text: str, file_path: str) -> None:
        text_bytes = text.encode('utf-8')
        with open(file_path, 'wb') as f:
            f.write(text_bytes)

    def load_text(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            texto_bytes = f.read()
            text = texto_bytes.decode('utf-8')
        return text

    def run(self, url: str, whisper_model: str = "base",
            max_characters: int = 500, email: str = None,
            voice: str = "media/voices/female_01.wav",
            voice_speed: float = 2, language: str = "pt",
            auto_play: bool = True, clean: bool = True) -> None:

        self.get_yt_audio(url)
        transcription = self.transcribe_audio(model=whisper_model)
        summary = self.resume(transcription, max_caracteres=max_characters)
        if email:
            self.send_email(summary, email)
        self.text_to_speak(summary, voice=voice, voice_speed=voice_speed,
                           language=language, auto_play=auto_play)

        if clean:
            if os.path.exists(self.AUDIO_PATH):
                os.remove(self.AUDIO_PATH)
            if os.path.exists(self.TRANSCRIPTION_PATH):
                os.remove(self.TRANSCRIPTION_PATH)
            if os.path.exists(self.SUMMARY_PATH):
                os.remove(self.SUMMARY_PATH)
