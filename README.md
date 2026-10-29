# Offline Multimodal AI Assistant

A privacy-first, no-API-key offline AI assistant that can run locally on any device with local inference.

## Features
- Offline text chat with local LLMs
- Speech input/output support
- Image input support
- Local memory logging
- Browser UI
- Easy deployment to local network or public server

## Requirements
- Python 3.11+
- Node.js 18+
- Ollama installed locally
- Optional: webcam, microphone, speakers

## Install Ollama
Linux/macOS:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Then install a model:

```bash
ollama pull llama3.2
```

## Backend setup
```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Frontend setup
```bash
cd app/frontend
npm install
npm run dev -- --host 0.0.0.0
```
