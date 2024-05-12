import yt_dlp as youtube_dl  # Replace 'youtube_dl' with 'yt_dlp'
from google.cloud import speech
import os

def download_video_extract_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'quiet': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return "downloaded_audio.wav"

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, 'rb') as audio:
        content = audio.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

def main():
    video_url = input("Enter the YouTube video URL: ")
    audio_file = download_video_extract_audio(video_url)
    print("Transcribing audio...")
    transcript = transcribe_audio(audio_file)
    print("Transcription:\n", transcript)

if __name__ == "__main__":
    main()
