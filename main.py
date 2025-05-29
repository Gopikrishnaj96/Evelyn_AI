import os
import eel
from engine.features import *
from engine.command import *
from engine.conversation import *
import threading
from engine.sentiment_analysis import predict_sentiment
from engine.emotion_analysis import analyze_video_emotion_snippet

def warmup_models():
    try:
        print("[INFO] Warming up models in background...")
        _ = predict_sentiment("Hello world")  # Dummy input
        print("[INFO] Sentiment model warmed up.")

        # Optional: create a fake lightweight mp4 if needed
        print("[INFO] Skipping real video for face model warmup.")
        _ = analyze_video_emotion_snippet("C:/Users/USER/Desktop/jarvis/output.mp4")
        print("[INFO] Emotion model ready.")

    except Exception as e:
        print("[ERROR] Model warmup failed:", e)

def start():
    warmup_thread = threading.Thread(target=warmup_models, daemon=True)
    warmup_thread.start()
    eel.init("www")

    @eel.expose
    def on_close():
        print("Frontend closed. Exiting backend...")
        os._exit(0)

    # Start model warmup in background
    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)