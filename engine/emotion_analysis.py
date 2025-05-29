import cv2
import numpy as np
import tensorflow as tf
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
model_path = "C:/Users/USER/Desktop/jarvis/models/face_emotion_detection_model.h5"
model = tf.keras.models.load_model(model_path)
def analyze_video_emotion_snippet(video_path):
    """
    Analyzes a video file to detect the dominant emotion in detected faces.

    Args:
        video_path (str): Path to the video file.

    Returns:
        str: The dominant emotion detected, or None if no valid emotions are detected.
    """
    # Configuration
    NEUTRAL_CONFIDENCE_THRESHOLD = 0.80  # For each frame: accept Neutral only if confidence ≥ 80%
    NEUTRAL_DOMINANCE_THRESHOLD = 0.80  # For final decision: accept Neutral only if it appears in >80% frames

    
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # Load the model and face detectoremoSS
    try:
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    except Exception as e:
        logging.error(f"Error loading model or face cascade: {e}")
        return None

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Error: Could not open video file: {video_path}")
        return None

    selected_emotions = []
    frame_count = 0
    logging.info("Analyzing the recorded video for face/emotion...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 10 != 0:  # Process every 10th frame
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (48, 48))
            face_roi = np.expand_dims(face_roi, axis=-1)
            face_roi = np.expand_dims(face_roi, axis=0)
            face_roi = face_roi / 255.0
            prediction = model.predict(face_roi)[0]

            sorted_indices = np.argsort(prediction)[::-1]

            for idx in sorted_indices:
                candidate_emotion = emotion_labels[idx]
                confidence = prediction[idx]

                if candidate_emotion == "Neutral" and confidence < NEUTRAL_CONFIDENCE_THRESHOLD:
                    continue

                selected_emotions.append(candidate_emotion)
                break

    cap.release()
    cv2.destroyAllWindows()

    if not selected_emotions:
        logging.warning("No valid emotions detected after filtering.")
        return None

    # Count the frequency of each emotion
    emotion_counts = Counter(selected_emotions)
    total_selected = sum(emotion_counts.values())

    # Final Decision Rule
    neutral_count = emotion_counts.get("Neutral", 0)
    neutral_ratio = neutral_count / total_selected

    if neutral_ratio > NEUTRAL_DOMINANCE_THRESHOLD:
        final_emotion = "Neutral"
    else:
        # Exclude 'Neutral' and return the next most common emotion
        emotion_counts.pop("Neutral", None)
        final_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else None

    logging.info(f"Final Detected Emotion: {final_emotion}")
    return final_emotion
