# 🤖 AI Customer Support Chatbot (RAG Based)

A real-time AI chatbot built using Retrieval-Augmented Generation (RAG) to provide intelligent customer support.

## 🚀 Features
- 🔍 RAG using FAISS vector database
- ⚡ Real-time streaming responses
- 🧠 Session-based chat memory (MongoDB)
- 🎤 Voice input + text-to-speech
- 💬 Chat history per session
- 🎨 Interactive React UI

## 🛠 Tech Stack
- Frontend: React, GSAP
- Backend: FastAPI, Node.js
- AI: Ollama (LLaMA 3)
- Database: MongoDB
- Vector DB: FAISS

## 📦 Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
