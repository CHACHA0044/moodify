# 🎵 Moodify - Emotion-Based Music Recommender

Detect your emotion through webcam or text and get personalized Spotify song recommendations!

## ✨ Features

- 📷 **Webcam Emotion Detection** - Uses DeepFace AI to analyze your facial expressions
- ✍️ **Text Emotion Analysis** - Detects emotions from what you type
- 🎶 **Smart Music Recommendations** - Curated Spotify playlists for every mood
- 🚀 **No Login Required** - Start using immediately
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile

## 🌐 Live Demo

**Frontend:** [https://chacha0044.github.io/moodify/](https://chacha0044.github.io/moodify/)

**Backend API:** [https://moodify-r2p0.onrender.com](https://moodify-r2p0.onrender.com)

## 🎭 Supported Emotions

- Happy / Joy
- Sad / Sadness
- Angry / Anger
- Fear
- Surprise
- Disgust
- Neutral
- Love

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Responsive Design
- Camera API Integration

### Backend
- Python Flask
- DeepFace (Facial Emotion Recognition)
- Transformers (Text Emotion Analysis)
- OpenCV
- Pandas

## 🚀 Local Development

### Prerequisites
- Python 3.9+
- Webcam (for facial emotion detection)

### Setup

1. Clone the repository
```bash
git clone https://github.com/CHACHA0044/moodify.git
cd moodify
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the server
```bash
python server.py
```

4. Open `docs/index.html` in your browser or use a local server:
```bash
python -m http.server 8080
```

Then visit: `http://localhost:8080/docs/`

## 📝 API Endpoints

### `POST /text`
Analyze emotion from text input
```json
{
  "text": "I'm feeling great today!"
}
```

### `POST /webcam`
Analyze emotion from webcam image
```json
{
  "image": "base64_encoded_image"
}
```

## 📄 License

MIT License - feel free to use this project!

## 🤝 Contributing

Pull requests are welcome! Feel free to improve the song database or add new features.

## 👨‍💻 Author

**PRANAV , SAHIM , NUMAN**

---

Made with ❤️ and 🎵