import os
import warnings
import logging

# Suppress TensorFlow and other unnecessary logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('deepface').setLevel(logging.ERROR)

from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import cv2
import base64
import numpy as np

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Keyword-based emotion detection for text
EMOTION_KEYWORDS = {
    'happy': ['happy', 'joy', 'joyful', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'good', 'excellent', 'love', 'loving', 'cheerful', 'delighted', 'pleased', 'glad'],
    'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable', 'crying', 'upset', 'heartbroken', 'disappointed', 'lonely', 'blue', 'melancholy'],
    'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'rage', 'frustrated', 'pissed', 'livid', 'outraged'],
    'fear': ['scared', 'afraid', 'fearful', 'anxious', 'worried', 'nervous', 'terrified', 'frightened', 'panic'],
    'surprise': ['surprised', 'shocked', 'amazed', 'wow', 'unexpected', 'astonished', 'stunned'],
    'disgust': ['disgusted', 'gross', 'yuck', 'horrible', 'awful', 'revolting', 'sick'],
    'love': ['love', 'adore', 'cherish', 'affection', 'romantic', 'caring', 'tender'],
    'neutral': ['okay', 'fine', 'alright', 'normal', 'meh', 'whatever']
}

def detect_text_emotion(text):
    """Detect emotion from text using keyword matching"""
    text_lower = text.lower()
    emotion_scores = {}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        detected = max(emotion_scores, key=emotion_scores.get)
        return detected
    
    return 'neutral'

@app.route("/")
def home():
    return jsonify({"message": "Moodify API is running!", "status": "ok"})

@app.route("/text", methods=["POST", "OPTIONS"])
def text_emotion():
    # Handle preflight request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response
    
    try:
        data = request.get_json()
        text = data.get("text", "")
        
        if not text:
            return jsonify({"error": "Text not provided"}), 400
        
        emotion = detect_text_emotion(text)
        response = jsonify({"emotion": emotion, "score": 0.95})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webcam", methods=["POST", "OPTIONS"])
def webcam_emotion():
    # Handle preflight request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response
    
    try:
        data = request.get_json()
        img_data = data.get("image")
        
        if not img_data:
            return jsonify({"error": "Image not provided"}), 400

        # Decode Base64 image
        img_bytes = base64.b64decode(img_data.split(',')[1])
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Analyze facial emotion using DeepFace
        result = DeepFace.analyze(img_path=img, actions=['emotion'], enforce_detection=False)
        dominant = result[0]['dominant_emotion']
        
        response = jsonify({"emotion": dominant})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)