from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from docx import Document
from pypdf import PdfReader
import io

router = APIRouter()

def extract_text_from_txt(data: bytes) -> str:
    return data.decode("utf-8", errors="ignore")

def extract_text_from_docx(data: bytes) -> str:
    doc = Document(io.BytesIO(data))
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    text_chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)
    return "\n".join(text_chunks)

@router.post("/document/extract")
async def extract_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".txt"):
            text = extract_text_from_txt(contents)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(contents)
        elif filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file type. Use .txt, .docx, or .pdf"}
            )

        return {
            "status": "ok",
            "filename": file.filename,
            "text": text[:3000],
            "message": "Document uploaded and extracted successfully."
        }

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
