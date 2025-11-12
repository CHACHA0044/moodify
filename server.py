#server.py
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

from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from deepface import DeepFace
from transformers import pipeline
import cv2
import base64
import numpy as np

app = Flask(__name__)
CORS(app)  # Add this line right after app creation

# Load text emotion model
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

@app.route("/")
def home():
    return jsonify({"message": "Moodify API is running!"})

@app.route("/text", methods=["POST"])
def text_emotion():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text not provided"}), 400
    result = emotion_model(text)[0]
    return jsonify({"emotion": result["label"], "score": result["score"]})

@app.route("/webcam", methods=["POST"])
def webcam_emotion():
    data = request.get_json()
    img_data = data.get("image")
    if not img_data:
        return jsonify({"error": "Image not provided"}), 400

    # Decode Base64 image
    img_bytes = base64.b64decode(img_data.split(',')[1])
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Analyze facial emotion
    result = DeepFace.analyze(img_path=img, actions=['emotion'], enforce_detection=False)
    dominant = result[0]['dominant_emotion']
    return jsonify({"emotion": dominant})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
