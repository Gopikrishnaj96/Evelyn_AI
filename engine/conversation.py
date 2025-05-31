import subprocess  # For running system commands like ffmpeg
import requests  # For making HTTP requests (e.g., to OpenAI's API)
import openai   # For interacting with OpenAI's API
import eel  # For Python-JavaScript communication in a hybrid application
import pyttsx3  # For text-to-speech functionality
from engine import video_audio_processing
import re
import os

#chat bot

openai.api_key = your_api_key
client = openai

"""system_prompt = (
   system_prompt = (
    "You're a warm, emotionally intelligent companion. "
    "In 30 words, respond based on both facial emotion and text sentiment, especially when they conflict. "
    "Reflect emotional tension. Be concise, thoughtful, and human-like. "
    "Avoid clichés. Personalize gently. Use warmth, not scripts."
)
"""
"""
system_prompt = (
     "You are a helpful and context-aware assistant. "
    "Respond thoughtfully based only on the user's text and conversation history. "
    "Use a neutral, informative tone. Limit responses to 30 words."
    )
"""
system_prompt = (
    "You are Evelyn, a perceptive, emotionally intelligent companion. "
    "In 30 words, respond to both the user's facial emotion and text sentiment, especially when they conflict. "
    "Detect emotional dissonance, be human-like, and empathetic. "
    "Personalize gently. Avoid generic replies. Use warmth, compassion, and insight. Prioritize emotional honesty."
    "warning: dont use emojis, if the emotions are neutral then dont go into an emotional conversation, "
)

def conversation_mode(video_filename,transcription):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # voices[1] is usually female
    engine.setProperty('rate', 174)  # Optional: adjust speech speed

    conversation_history = []
    MAX_HISTORY_TURNS = 5
    i=0
    print("[INFO] Conversation mode started. Say 'stop' to end the conversation.")
    while True:
        # Stop condition
        from engine.emotion_analysis import analyze_video_emotion_snippet
        from engine.sentiment_analysis import predict_sentiment
        from engine.memory_management import store_memory, retrieve_memories, summarize_history, chroma_client,clear_memory_collection
        a = [
             ["Neutral", "Neutral"],
            ["Sad", "Positive"],
            ["Neutral", "Positive"],
            ["Sad", "Positive"],
            ["Happy", "Positive"],
            ["Neutral", "Positive"]]        
        if "stop" in transcription.lower():
            engine.say("Goodbye.")
            print("Goodbye")
            
            eel.DisplayMessage("Goodbye")
            eel.receiverText("Goodbye")
            engine.runAndWait()
            # DELETE the collection before exiting
            #clear_memory_collection()
            return True
        
        video_emotion = analyze_video_emotion_snippet("output.mp4") or "Unknown"
        # Predict text sentiment
        sentiment = predict_sentiment(transcription)
        #video_emotion=a[i][0]
        #sentiment=a[i][1]
        i+=1
        #Print detected emotions
        print(f"[INFO] Detected Face Emotion: {video_emotion}")
        print(f"[INFO] Detected Text Sentiment: {sentiment}")
        eel.DisplayMessage(f"Detected video & text Emotion: {video_emotion},{sentiment}")
        eel.receiverText(f"Detected video & text Emotion: {video_emotion},{sentiment}")
        #Prepare user message without storing emotions in memory
        user_message = f"User said: {transcription}."
        store_memory(user_message, metadata={"type": "user"})

        # Summarize history if needed
        if len(conversation_history) > MAX_HISTORY_TURNS:
            summary = summarize_history(conversation_history[:-MAX_HISTORY_TURNS])
            store_memory(summary, metadata={"type": "summary"})
            conversation_history = conversation_history[-MAX_HISTORY_TURNS:]
            print("\n[DEBUG] === Summarization Triggered ===")
            print("Summary Input:", conversation_history[:-MAX_HISTORY_TURNS])
            print("Stored Summary:", summary)
        # Retrieve context
        context_snippets = retrieve_memories(transcription, top_k=3)
        context_block = "\n".join(context_snippets)
         # Compact intelligent prompt
        #compact_prompt = f"""
         #              User: {transcription}
          #              """
        # Compact intelligent prompt
        compact_prompt = f"""
                        Context: {context_block}
                        User: {transcription}
                        Emotion: {video_emotion} | Sentiment: {sentiment}
                        """ 
        # Print the full prompt for debug/logging
        print("\n[DEBUG] === Prompt Sent to GPT ===")
        print(f"System Prompt:\n{system_prompt}\n")
        print(f"User Prompt:\n{compact_prompt}")
        print("==================================\n")

        # Generate assistant response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": compact_prompt}
            ],
            temperature=0.7,
            max_tokens=150
        ).choices[0].message.content.strip()

        # Print and speak assistant response
        print("Assistant:", response)
        eel.DisplayMessage(response)
        engine.say(response)
        eel.receiverText(response)
        engine.runAndWait()

       # Add to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Store assistant response
        store_memory(response, metadata={"type": "assistant_response"})
        conversation_history.append({"role": "assistant", "content": response})
        """
        Records video with audio, extracts audio, transcribes it, and returns the video file and transcription.
        """
        print("listening....")
        eel.DisplayMessage("listening....")
        
        # Record video with audio
        video_audio_processing.record_video_with_audio(duration=8, output_filename=video_filename)
        print("[INFO] Recording complete.")
        # Extract audio from the video
        eel.DisplayMessage("recognizing")
        audio_filename = "output_audio.wav"
        video_audio_processing.extract_audio_from_video(video_filename, audio_filename)
        
        # Transcribe audio
        transcription = video_audio_processing.transcribe_audio_with_openai(audio_filename)
        transcription =transcription.lower()
        print("[INFO] Transcribed Text:", transcription)
        eel.DisplayMessage(transcription)
        eel.senderText(transcription)
        
def record_video_with_audio(duration=8, output_filename="output.mp4"):
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
