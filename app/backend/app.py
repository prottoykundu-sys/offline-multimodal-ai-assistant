from fastapi import FastAPI, UploadFile, File, HTTPException
from routes.chat import router as chat_router
from routes.voice import router as voice_router
from routes.vision import router as vision_router
from routes.document import router as document_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import uuid
import tempfile
from pathlib import Path

app = FastAPI(title="Offline Multimodal AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(voice_router, prefix="/api")
app.include_router(vision_router, prefix="/api")
app.include_router(document_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "offline-multimodal-ai-assistant"}

@app.get("/")
async def root():
    return {"message": "Offline Multimodal AI Assistant"}
