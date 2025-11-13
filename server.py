import os
import warnings
import logging
import sys
from threading import Thread
import time
import requests

# Suppress TensorFlow and other unnecessary logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('deepface').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import cv2
import base64
import numpy as np
import gc

# Force garbage collection periodically
def cleanup_memory():
    gc.collect()
app = Flask(__name__)

# Enable CORS - Allow all origins
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "supports_credentials": False
    }
})

# Add CORS headers to ALL responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Origin'] = origin if origin != '*' else '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, HEAD'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response

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

# Self-ping function to keep server awake
def keep_alive():
    """Ping the server every 3 minutes to prevent Render from sleeping"""
    time.sleep(60)  # Wait 1 minute after startup
    
    while True:
        try:
            # Get the Render URL from environment or use default
            render_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://moodify-r2p0.onrender.com')
            
            # Ping the health endpoint
            response = requests.get(f'{render_url}/ping', timeout=10)
            if response.status_code == 200:
                print(f"[KEEP-ALIVE] ✓ Pinged at {time.strftime('%H:%M:%S')}", file=sys.stderr)
            else:
                print(f"[KEEP-ALIVE] ⚠ Ping returned {response.status_code}", file=sys.stderr)
        except Exception as e:
            print(f"[KEEP-ALIVE] ✗ Ping failed: {str(e)}", file=sys.stderr)
        
        # Wait 3 minutes before next ping
        time.sleep(180)

@app.route("/")
def home():
    return jsonify({
        "message": "Moodify API is running!", 
        "status": "ok",
        "version": "1.0",
        "endpoints": {
            "ping": "/ping - GET - Wake up check",
            "text": "/text - POST - Analyze emotion from text",
            "webcam": "/webcam - POST - Analyze emotion from image"
        }
    }), 200

@app.route("/ping", methods=["GET", "OPTIONS"])
def ping():
    """Lightweight endpoint to wake up the server"""
    if request.method == "OPTIONS":
        return '', 204
    return jsonify({"status": "awake", "message": "Server is ready"}), 200

@app.route("/text", methods=["POST", "OPTIONS"])
def text_emotion():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return '', 204
    
    try:
        # Get JSON data
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "Text field is required"}), 400
        
        # Detect emotion
        emotion = detect_text_emotion(text)
        
        return jsonify({
            "emotion": emotion, 
            "score": 0.95,
            "method": "keyword-based"
        }), 200
    
    except Exception as e:
        print(f"[TEXT] Error: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route("/webcam", methods=["POST", "OPTIONS"])
def webcam_emotion():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return '', 204
    
    try:
        # Get JSON data
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        img_data = data.get("image")
        
        if not img_data:
            return jsonify({"error": "Image field is required"}), 400

        # Decode Base64 image with reduced quality
        try:
            # Handle data URL format
            if ',' in img_data:
                img_data = img_data.split(',')[1]
            
            # Add padding if needed
            missing_padding = len(img_data) % 4
            if missing_padding:
                img_data += '=' * (4 - missing_padding)
            
            img_bytes = base64.b64decode(img_data)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Failed to decode image"}), 400
            
            # Resize to smaller dimensions for faster processing
            height, width = img.shape[:2]
            max_size = 480
            
            if width > max_size or height > max_size:
                scale = max_size / max(width, height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = cv2.resize(img, (new_width, new_height))
                print(f"[WEBCAM] Resized to {new_width}x{new_height}", file=sys.stderr)
                
        except Exception as e:
            print(f"[WEBCAM] Decode error: {str(e)}", file=sys.stderr)
            return jsonify({"error": f"Image decode failed: {str(e)}"}), 400
        # Analyze facial emotion using DeepFace
        try:
            result = DeepFace.analyze(
                img_path=img, 
                actions=['emotion'], 
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            # Handle both list and dict responses
            if isinstance(result, list):
                dominant = result[0]['dominant_emotion']
            else:
                dominant = result['dominant_emotion']
            
            # Clean up memory immediately
            del img, nparr, img_bytes
            
            return jsonify({
                "emotion": dominant,
                "method": "deepface"
            }), 200
            
        except Exception as e:
            print(f"[WEBCAM] DeepFace error: {str(e)}", file=sys.stderr)
            
           # Clean up memory
            try:
                del img, nparr, img_bytes
            except:
                pass
            
            gc.collect()  # Force garbage collection
            
            # Return neutral as fallback
            return jsonify({
                "emotion": "neutral",
                "warning": "Face detection failed, using neutral",
                "method": "fallback",
                "error_detail": str(e)
            }), 200
    
    except Exception as e:
        print(f"[WEBCAM] General error: {str(e)}", file=sys.stderr)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    print("=" * 60, file=sys.stderr)
    print(f"🎵 Moodify API Server Started", file=sys.stderr)
    print(f"   Port: {port}", file=sys.stderr)
    print(f"   CORS: Enabled", file=sys.stderr)
    print(f"   Keep-Alive: Active (3 min interval)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Start keep-alive thread to prevent Render from sleeping
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)