from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import requests
import base64

router = APIRouter()

@router.post("/vision/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("Describe this image in detail.")
):
    try:
        contents = await file.read()
        encoded = base64.b64encode(contents).decode("utf-8")

        payload = {
            "model": "llava",
            "prompt": prompt,
            "stream": False,
            "images": [encoded]
        }

        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=180
        )

        response.raise_for_status()
        result = response.json()

        return {
            "status": "ok",
            "response": result.get("response", ""),
            "model": "llava"
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
