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


def get_transcription(url: str) -> str:
    """
    Retrieves the transcription of a YouTube video.

    Parameters:
    url (str): URL of the YouTube video.

    Returns:
    str: The transcription of the video.
    """
    transcript = ""
    video_id = url.split("=")[1]
    responses = YouTubeTranscriptApi.get_transcript(
        video_id, languages=['pt'])
    for r in responses:
        transcript += " " + r["text"]
    return transcript


def summarize_transcription(transcription: str, max_words: int, gemini_api_key: str, language: str) -> str:
    """
    Summarizes the transcription of a YouTube video using a Google Gemini.

    Parameters:
    transcription (str): The transcription of a video.
    max_words (int): The maximum number of words in the summary.
    gemini_api_key (str): The API key for Gemini to access the generative model.

    Returns:
    str: The summary of the transcription.
    """
    prompt = f"""Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcription into a concise summary without special characters in {language}. Your summary should also capture the main points and essential information within a limit of {max_words} words. Let's dive into the provided transcription and extract the vital details for our audience."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')
    response = model.generate_content(prompt + transcription)
    return response.text


def send_email(text: str, to_email: str, from_email: str, from_email_password: str, subject: str):
    """
    Sends an email with the provided text.

    Parameters:
    text (str): The content of the email.
    to_email (str): The recipient's email address.
    from_email (str): The sender's email address.
    from_email_password (str): The password for the sender's email.
    subject (str): The subject of the email.

    Returns:
    None
    """
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


def speak(text: str, google_cloud_account: str,
          language_code: str, voice_name: str, speaking_rate: float = 1,
          auto_play: bool = True):
    """
    Converts text to speech using the Google Cloud Text-to-Speech API and plays the generated audio.

    Parameters:
    text: The text to be converted to speech.
    google_cloud_account: The path to the Google Cloud service account credentials file.
    language_code: Language code of the voice chosen on Google Cloud Text-To-Speech
    voice_name: Voice name chosen on Google Cloud Text-To-Speech
    auto_play: If True, automatically plays the generated audio. Default is True.
    speaking_rate: Speaking rate/speed, in the range [0.25, 4.0]. Default is 1.
    Returns:
    None
    """
    credentials = service_account.Credentials.from_service_account_file(
        google_cloud_account)
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    si = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['small-bluetooth-speaker-class-device'],
        speaking_rate=speaking_rate,
        pitch=1
    )

    response = client.synthesize_speech(
        input=si,
        voice=voice,
        audio_config=audio_config
    )

    output_filename = 'output.mp3'

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print('Audio download done', color='green')

    sound = AudioSegment.from_mp3(output_filename)

    if auto_play:
        play(sound)
