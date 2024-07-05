# Video Summarizer

This project is a video summarizer tool that extracts transcriptions from YouTube videos, summarizes them using a generative AI model, converts the summaries to speech, and sends them via email.

Demonstration: [LinkedIn](https://www.linkedin.com/posts/matheus-gr_llama3-whisper-elevenlabs-activity-7212213971062312960-s12O?utm_source=share&utm_medium=member_desktop)

## Features

- **Transcription**: Extracts the transcription of a YouTube video.
- **Translate**: Translate the transcription if requested.
- **Summarization**: Summarizes the transcription using a generative AI model.
- **Text-to-Speech**: Converts the summary to speech using Google Cloud Text-to-Speech API.
- **Email Sending**: Sends the summarized text via email.

## Requirements

- `Python 3.11+`
- `Anaconda or miniconda`

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Matheus-Gr/Video-Ai-Summarizer.git
   cd Video-Ai-Summarizer
   ```

2. Create a `conda` virtual environment and activate it:

   ```sh
   conda env create -f environment.yml
   conda activate summarize
   ```

3. You will need a google service account in a `credentials.json` file in the project root folder. Recomend watch this [tutorial](https://youtu.be/DtlJH6MgBso?si=ghEd3QDVtnGnzO3N&t=64) from Parwiz Forogh Youtube Chanell.

## Usage

1. **Set Up Environment Variables**:
   Ensure the following environment variables are set in your environment:

   - `gemini_key`: Your API key for Gemini.
   - `google_cloud`: Json containg yout Google Cloud Credentials.
   - `to_mail`: The recipient's email address.
   - `from_email`: The sender's email address.
   - `from_email_password`: The sender's email password.

2. **Set Up Summary Options**

   - `max_words`: Maximum of words on summary.
   - `languague`: The language of the summary. This string should be fully specified, such as "American English" or "Brazilian Portuguese". If the chosen language is different from the video's language, the summary will be automatically translated.

3. **Set Up Voice Options**: Custom you voice and language preferences:

   - `language_code`: Language code of the voice chosen on Google Cloud Text-To-Speech.
   - `voice_name`: Voice name chosen on Google Cloud Text-To-Speech.
   - `speaking_rate`: Speed of the output audio.

   _To chose a voice you can visit [voice list](https://cloud.google.com/text-to-speech/docs/voices) on google cloud site._

4. **Run the Notebook**: Put your YouTube video link and run the notebook:

   - `video_url`: YouTube video url. The video cannot be under any type of restrictions, like age restriction or private videos.

   Run the `video_summarizer.ipynb` notebook on `summarize` enviroment.

## Functions

### `get_transcription(url: str) -> str`

Retrieves the transcription of a YouTube video.

- **Parameters**:
  - `url` (str): URL of the YouTube video.
- **Returns**:
  - `str`: The transcription of the video.

### `summarize_transcription(transcription: str, max_words: int, gemini_api_key: str, language: str) -> str`

Summarizes the transcription of a YouTube video using a generative model.

- **Parameters**:
  - `transcription` (str): The transcription of the video.
  - `max_words` (int): The maximum number of words in the summary.
  - `gemini_api_key` (str): The API key for Gemini to access the generative model.
  - `language` (str): The language of the transcription.
- **Returns**:
  - `str`: The summary of the transcription.

### `send_email(text: str, to_email: str, from_email: str, from_email_password: str, subject: str)`

Sends an email with the provided text.

- **Parameters**:
  - `text` (str): The content of the email.
  - `to_email` (str): The recipient's email address.
  - `from_email` (str): The sender's email address.
  - `from_email_password` (str): The password for the sender's email.
  - `subject` (str): The subject of the email.
- **Returns**:
  - None

### `speak(text: str, google_cloud_account: str, language_code: str, voice_name: str, auto_play: bool = True)`

Converts text to speech using the Google Cloud Text-to-Speech API and plays the generated audio.

- **Parameters**:
  - `text` (str): The text to be converted to speech.
  - `google_cloud_account` (str): The path to the Google Cloud service account credentials file.
  - `language_code` (str): The language code for the voice (e.g., "pt-BR").
  - `voice_name` (str): The name of the voice (e.g., 'pt-BR-Wavenet-C').
  - `speaking_rate` (float): Speaking rate/speed, in the range [0.25, 4.0]. Default is 1.
  - `auto_play` (bool): If True, automatically plays the generated audio. Default is True.
- **Returns**:
  - None

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [pytube](https://github.com/nficano/pytube)
- [pydub](https://github.com/jiaaro/pydub)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [Gemini Generative AI](https://gemini.com/)
