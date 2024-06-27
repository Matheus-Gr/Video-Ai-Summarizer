from pydub.playback import play
from pydub import AudioSegment
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
from print_color import print
from google.cloud import texttospeech
from google.oauth2 import service_account
from email.message import EmailMessage
import ssl
import smtplib


def speak(text: str, auto_play: bool = True):
    credentials = service_account.Credentials.from_service_account_file(
        'summarizer_account.json')
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    si = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name='pt-BR-Wavenet-C'
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['small-bluetooth-speaker-class-device'],
        speaking_rate=1,
        pitch=1
    )

    response = client.synthesize_speech(
        input=si,
        voice=voice,
        audio_config=audio_config
    )

    with open('output.mp3', "wb") as out:
        out.write(response.audio_content)
        print('Saved')

    sound = AudioSegment.from_mp3('output.mp3')

    if auto_play:
        play(sound)


def get_transcription(url: str) -> str:
    transcript = ""
    video_id = url.split("=")[1]
    responses = YouTubeTranscriptApi.get_transcript(
        video_id, languages=['pt'])
    for r in responses:
        transcript += " " + r["text"]
    return transcript


def summarize_transcription(transcription: str, max_words: int) -> str:
    prompt = f"""Bem-vindo, Video Summarizer! Sua tarefa é destilar a essência de uma determinada transcrição de vídeo do YouTube em um resumo conciso. Seu resumo deve capturar os pontos principais e as informações essenciais, apresentadas em marcadores, dentro de um limite de {max_words} palavras. Vamos mergulhe na transcrição fornecida e extraia os detalhes vitais para nosso público."""
    genai.configure(api_key=os.getenv('GEMINI_KEY'))
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')
    response = model.generate_content(prompt + transcription)
    return response.text


def send_email(text: str, to_email: str):
    subject = "Resumo do video"
    from_email = os.getenv('EMAIL')
    from_email_password = os.getenv('EMAIL_PASSWORD')
    body = text
    em = EmailMessage()

    em['From'] = from_email
    em['To'] = to_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(from_email, from_email_password)
        smtp.sendmail(from_email, to_email, em.as_string())
    print("Email sent!", color='green')


url = 'https://www.youtube.com/watch?v=On2Yx349neE'
max_words = 250

t = get_transcription(url)
print(t)
s = summarize_transcription(t, max_words)
print(s)
speak(s)
