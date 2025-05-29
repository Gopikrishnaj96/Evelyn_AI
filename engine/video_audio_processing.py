import subprocess
import requests
from openai import OpenAI  # For interacting with OpenAI's API
client = OpenAI(api_key="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")  # Replace with your actual key
import eel

def record_video_with_audio(duration=8, output_filename="output.mp4"):
    eel.DisplayMessage("recognizing")
    """
    Records a video with audio using ffmpeg.

    Args:
        duration (int): Duration of the video in seconds.
        output_filename (str): Name of the output video file.
    """
    command = [
        'ffmpeg',
        '-y',
        '-f', 'dshow',
        '-i', 'audio=Microphone Array (Realtek(R) Audio)',
        '-f', 'dshow',
        '-i', 'video=USB2.0 HD UVC WebCam',
        '-t', str(duration),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        output_filename
    ]
    subprocess.run(command)

def extract_audio_from_video(video_file, audio_file):
    """
    Extracts audio from a video file using ffmpeg.

    Args:
        video_file (str): Path to the input video file.
        audio_file (str): Path to the output audio file.
    """
    command = [
        'ffmpeg',
        '-y',
        '-i', video_file,
        '-vn',
        '-ar', '16000',
        '-ac', '1',
        '-c:a', 'pcm_s16le',
        audio_file
    ]
    subprocess.run(command)

def transcribe_audio_with_openai(audio_filename="output_audio.wav"):
    """
    Transcribes audio using OpenAI's Whisper API.

    Args:
        audio_filename (str): Path to the audio file to transcribe.

    Returns:
        str: Transcribed text from the audio file.
    """
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {client.api_key}"}  # Use the client object for the API key
    with open(audio_filename, "rb") as audio_file:
        files = {"file": (audio_filename, audio_file, "audio/wav")}
        data = {"model": "whisper-1", "language": "en"}
        response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print("[ERROR] Failed to transcribe:", response.json())
        return ""