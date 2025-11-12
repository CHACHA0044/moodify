#app.py
import os
import warnings
import logging

# Suppress TensorFlow and other unnecessary logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 3 = only fatal errors
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configure logging to show only essential info
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('deepface').setLevel(logging.ERROR)
logging.getLogger('huggingface_hub').setLevel(logging.ERROR)

import cv2
import pandas as pd
import random
from deepface import DeepFace
from transformers import pipeline
from collections import defaultdict

# Load Hugging Face model for text emotion detection
print("Loading Hugging Face emotion model...")
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Load songs database
songs_df = pd.read_csv("songs.csv")
last_recommended = defaultdict(lambda: None)

# -----------------------------
# Helper Functions
# -----------------------------
def get_random_song(emotion):
    """Return a random non-repeating song for a detected emotion."""
    available_songs = songs_df[songs_df['emotion'].str.lower() == emotion.lower()]
    if available_songs.empty:
        return None

    songs_list = available_songs.to_dict('records')
    if last_recommended[emotion]:
        songs_list = [s for s in songs_list if s['song_name'] != last_recommended[emotion]['song_name']]

    song = random.choice(songs_list)
    last_recommended[emotion] = song
    return song


def detect_emotion_from_text(text):
    """Detect emotion from text input using Hugging Face."""
    result = emotion_classifier(text, truncation=True)[0]
    emotion = result['label'].lower()
    print(f"\n🧠 Detected text emotion: {emotion}")
    return emotion


def detect_emotion_from_webcam():
    """Detect dominant emotion from live webcam feed."""
    print("\n🎥 Opening webcam... Press 'q' to capture emotion.")
    cap = cv2.VideoCapture(0)
    detected_emotion = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Could not access webcam.")
            break

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        cv2.putText(frame, f"Emotion: {emotion}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Moodify - Press 'q' to capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            detected_emotion = emotion
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🎭 Detected facial emotion: {detected_emotion}")
    return detected_emotion


def recommend_music(emotion):
    """Recommend a random song for a given emotion."""
    song = get_random_song(emotion)
    if song:
        print(f"\n🎶 Recommended song for '{emotion}':")
        print(f"→ {song['song_name']} by {song['artist']}")
        print(f"🔗 {song['link']}\n")
    else:
        print(f"No songs found for '{emotion}' emotion.\n")


# -----------------------------
# Main Loop
# -----------------------------
if __name__ == "__main__":
    print("=== MOODIFY 🎵 - Emotion Based Music Recommender ===")

    while True:
        print("\nSelect input type:")
        print("1. Webcam (facial emotion)")
        print("2. Text (type mood)")
        print("3. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            emotion = detect_emotion_from_webcam()
            if emotion:
                recommend_music(emotion)

        elif choice == "2":
            text = input("Enter how you feel: ")
            emotion = detect_emotion_from_text(text)
            recommend_music(emotion)

        elif choice == "3":
            print("👋 Exiting Moodify. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
