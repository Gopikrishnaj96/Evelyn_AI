# Evelyn: A Multimodal Sentiment-Aware Desktop Voice Assistant

**Evelyn** is a real-time desktop voice assistant that delivers emotionally intelligent responses by combining voice input, facial emotion recognition, and sentiment analysis. 
Designed to create natural and supportive interactions, Evelyn uses your webcam and microphone to analyze your emotions and tone before generating responses. It features a sleek
web-based chat interface powered by Python's Eel framework.

Evelyn integrates OpenAI Whisper for speech recognition, a CNN-based facial emotion detection model for analyzing video input, and a DistilBERT-based NLP model for classifying 
sentiment from text. It also retains conversation context using ChromaDB and SentenceTransformers to provide more coherent and memory-aware interactions.

You can trigger Evelyn with a hotword like "Jarvis" or interact via voice or typed input. The assistant can launch applications, play YouTube videos, send WhatsApp messages, and 
handle general queries with emotionally aware dialogue generated through GPT-4o.

---
![image](https://github.com/user-attachments/assets/0ace1bdd-1064-406d-b565-06dd92688c16)![image](https://github.com/user-attachments/assets/89ebf1c3-5db1-4607-9467-8518ce43de9b)



## 🌟 Features

- 🎙️ **Voice Transcription** with Whisper for seamless audio input.
- 😐 **Facial Emotion Detection** using a CNN model on live webcam input.
- 💬 **Sentiment Analysis** with DistilBERT for classifying text as positive, negative, or neutral.
- 🧠 **Context-Aware Conversations** using ChromaDB and sentence embeddings for memory recall.
- 🗣️ **Voice Output** with pyttsx3 for spoken responses.
- 🧩 **Command Execution**: Open apps, play music on YouTube, send WhatsApp messages or initiate calls.
- 🔥 **Hotword Activation** using Porcupine (Evelyn).
---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- `ffmpeg` installed and added to PATH
- Webcam and microphone

### Installation

```bash
git clone https://github.com/Gopikrishnaj96/Evelyn.git
cd Evelyn
pip install -r requirements.txt
