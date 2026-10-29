from fastapi import APIRouter
from pydantic import BaseModel
from models import LocalModelClient

router = APIRouter()
client = LocalModelClient()

class ChatRequest(BaseModel):
    model: str = "llama3.2"
    prompt: str
    document_text: str = ""

@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        if req.document_text:
            final_prompt = (
                "Use ONLY the uploaded document content below. "
                "Do not use outside knowledge. "
                "If the answer is not in the document, say so.\n\n"
                f"Document Content:\n{req.document_text}\n\n"
                f"Question:\n{req.prompt}"
            )
        else:
            final_prompt = req.prompt

        result = client.generate(
            model=req.model,
            prompt=final_prompt,
            system="You are a local offline AI assistant. Answer strictly from the provided input. Do not invent facts.",
            stream=False
        )

        return {"response": result.get("response", "")}
    except Exception as e:
        return {"error": str(e)}
