# 🎵 Moodify - Your Mood, Your Music

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://chacha0044.github.io/moodify/)
[![API Status](https://img.shields.io/badge/API-active-blue)](https://moodify-r2p0.onrender.com)
[![License](https://img.shields.io/badge/license-MIT-purple)](LICENSE)

> An intelligent emotion-based music recommendation system that analyzes your mood through facial expressions or text input and suggests the perfect Spotify tracks to match your feelings.

<div align="center">
  
<div align="center">
  <img src="https://raw.githubusercontent.com/CHACHA0044/moodify/main/docs/logo.svg" alt="Moodify Logo" width="180"/>
</div>
  
  ### *Discover music that matches your mood*
  
  <p align="center">
    <a href="#-features">Features</a> •
    <a href="#-live-demo">Demo</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-api-documentation">API</a> •
    <a href="#-contributing">Contributing</a>
  </p>
  
</div>

---

## ✨ Features

### 🎭 Dual Emotion Detection
- **📷 Webcam Mode**: Real-time facial emotion recognition using DeepFace AI
- **✍️ Text Mode**: Natural language emotion analysis with keyword-based detection

### 🎶 Smart Music Recommendations
- Curated library of 100+ songs across 10+ emotional categories
- Random non-repeating song selection for variety
- Direct Spotify integration with one-click playback
- Dynamic song cards with smooth animations

### 🚀 Production-Ready Features
- **Auto Wake-Up System**: Server keeps itself alive with 3-minute ping intervals
- **Optimized Performance**: Image compression and memory management
- **CORS Enabled**: Full cross-origin support for frontend-backend communication
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Responsive Design**: Seamless experience across desktop, tablet, and mobile

## 🌐 Live Demo

| Component | URL |
|-----------|-----|
| **Frontend** | [https://chacha0044.github.io/moodify/](https://chacha0044.github.io/moodify/) |
| **Backend API** | [https://moodify-r2p0.onrender.com](https://moodify-r2p0.onrender.com) |
| **Health Check** | [https://moodify-r2p0.onrender.com/ping](https://moodify-r2p0.onrender.com/ping) |

## 🎭 Supported Emotions

| Emotion | Sample Songs | Total Tracks |
|---------|-------------|--------------|
| 😊 Happy/Joy | "Can't Stop the Feeling!", "Happy" | 18 |
| 😢 Sad/Sadness | "Someone Like You", "Fix You" | 24 |
| 😠 Angry/Anger | "In the End", "Lose Yourself" | 17 |
| 😰 Fear | "Demons", "Radioactive" | 10 |
| 😲 Surprise | "Firework", "Wake Me Up" | 8 |
| 🤢 Disgust | "Bad Guy", "Toxic" | 7 |
| 😐 Neutral | "Blinding Lights", "Levitating" | 11 |
| ❤️ Love | "Perfect", "All of Me" | 15 |

## 🛠️ Tech Stack

### Frontend
```
HTML5 + CSS3 + Vanilla JavaScript
├── Responsive Grid Layout
├── CSS Animations & Transitions
├── Camera API Integration
├── Base64 Image Encoding
└── Fetch API for Backend Communication
```

### Backend
```python
Python 3.9+ Flask Application
├── Flask 3.0.0 (Web Framework)
├── DeepFace 0.0.93 (Facial Emotion Recognition)
├── OpenCV 4.10 (Image Processing)
├── TensorFlow 2.15+ (Deep Learning Backend)
├── Pandas (CSV Data Management)
├── Flask-CORS (Cross-Origin Support)
└── Gunicorn (Production Server)
```

### Infrastructure
- **Hosting**: Render.com (Backend), GitHub Pages (Frontend)
- **Keep-Alive**: Automated self-ping system (3-minute intervals)
- **Memory Management**: Garbage collection and image optimization

## 📦 Project Structure

```
moodify/
├── docs/
│   └── index.html          # Frontend application
├── server.py               # Flask API server
├── app.py                  # Original CLI version (legacy)
├── songs.csv               # Music database (110+ songs)
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── .gitignore             # Git exclusions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Webcam (for facial detection)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CHACHA0044/moodify.git
cd moodify
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
python server.py
```

Server will start on `http://localhost:8000`

5. **Launch the frontend**
```bash
# Option 1: Direct file access
open docs/index.html

# Option 2: Local HTTP server
cd docs
python -m http.server 8080
```

Visit `http://localhost:8080` in your browser

## 📡 API Documentation

### Base URL
```
Production: https://moodify-r2p0.onrender.com
Local: http://localhost:8000
```

### Endpoints

#### `GET /ping`
**Health check endpoint** - Wakes up the server

**Response:**
```json
{
  "status": "awake",
  "message": "Server is ready"
}
```

---

#### `POST /text`
**Analyze emotion from text input**

**Request Body:**
```json
{
  "text": "I'm feeling amazing today!"
}
```

**Response:**
```json
{
  "emotion": "happy",
  "score": 0.95,
  "method": "keyword-based"
}
```

**Supported Keywords:**
- `happy`: happy, joy, excited, great, wonderful, amazing
- `sad`: sad, depressed, down, unhappy, miserable, crying
- `angry`: angry, mad, furious, annoyed, irritated, rage
- `fear`: scared, afraid, anxious, worried, nervous
- `surprise`: surprised, shocked, amazed, wow
- `disgust`: disgusted, gross, yuck, horrible
- `love`: love, adore, cherish, romantic
- `neutral`: okay, fine, alright, normal

---

#### `POST /webcam`
**Analyze emotion from webcam image**

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "emotion": "happy",
  "method": "deepface"
}
```

**Error Response (with fallback):**
```json
{
  "emotion": "neutral",
  "warning": "Face detection failed, using neutral",
  "method": "fallback",
  "error_detail": "No face detected"
}
```

## 🎨 Frontend Features

### Camera Mode
- Live video preview with mirror effect
- One-click emotion capture
- Photo preview before processing
- Automatic camera shutdown after capture (memory optimization)

### Text Mode
- Large text input area
- Real-time emotion analysis
- Support for complex emotional expressions

### Results Display
- Animated emotion badge
- 3 random song recommendations per emotion
- Direct Spotify links
- Smooth card animations with staggered reveals

## ⚙️ Configuration

### Environment Variables

```bash
# Server Configuration
PORT=8000
FLASK_DEBUG=False

# Render Auto-Wake (for production)
RENDER_EXTERNAL_URL=https://moodify-r2p0.onrender.com
```

### Frontend Configuration

Update the API URL in `docs/index.html`:
```javascript
const API_URL = 'http://localhost:8000'; // For local development
// const API_URL = 'https://moodify-r2p0.onrender.com'; // For production
```

## 🔧 Advanced Usage

### Adding New Songs

Edit `songs.csv`:
```csv
emotion,name,artist,link
happy,Your Song Name,Artist Name,https://open.spotify.com/track/TRACKID
```

Supported emotions: `happy`, `joy`, `sad`, `sadness`, `angry`, `anger`, `fear`, `surprise`, `disgust`, `neutral`, `love`

### Customizing Emotion Keywords

Edit `EMOTION_KEYWORDS` dictionary in `server.py`:
```python
EMOTION_KEYWORDS = {
    'happy': ['happy', 'joy', 'excited', 'your-custom-keyword'],
    # Add more keywords...
}
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to server"
**Solution:** 
- Check if server is running (`python server.py`)
- Wait 30-60 seconds for Render to wake up (first request)
- Verify API_URL in frontend matches your server

### Issue: "Camera not working"
**Solution:**
- Grant camera permissions in browser
- Use HTTPS or localhost (required for camera access)
- Check if camera is not in use by another application

### Issue: "No emotion detected"
**Solution:**
- Ensure good lighting for webcam mode
- Face camera directly
- Try text mode as alternative
- Check browser console for detailed errors

## 📊 Performance Optimization

### Image Processing
- Resolution capped at 480x360 pixels
- JPEG compression at 40% quality
- Immediate memory cleanup after processing

### Server Management
- TensorFlow logging suppressed
- Garbage collection after each request
- Auto wake-up ping every 3 minutes
- Graceful fallback to neutral emotion

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Ideas
- 🎵 Expand song database
- 🌍 Add multi-language support
- 🎨 Improve UI/UX design
- 🤖 Integrate more emotion detection models
- 📱 Create mobile app version

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

**PRANAV, SAHIM, NUMAN**

- GitHub: [@CHACHA0044](https://github.com/CHACHA0044)

## 🙏 Acknowledgments

- [DeepFace](https://github.com/serengil/deepface) - Facial emotion recognition
- [Spotify](https://spotify.com) - Music streaming platform
- [Render](https://render.com) - Backend hosting
- [GitHub Pages](https://pages.github.com) - Frontend hosting

## 📈 Future Roadmap

- [ ] User accounts and listening history
- [ ] Playlist generation
- [ ] Social sharing features
- [ ] Integration with more music platforms (Apple Music, YouTube Music)
- [ ] Advanced emotion tracking over time
- [ ] Mobile app (iOS/Android)
- [ ] Voice emotion detection
- [ ] Collaborative playlist building

---

<div align="center">

Made with ❤️ and 🎵

**[Live Demo](https://chacha0044.github.io/moodify/)** • **[Report Bug](https://github.com/CHACHA0044/moodify/issues)** • **[Request Feature](https://github.com/CHACHA0044/moodify/issues)**

</div>