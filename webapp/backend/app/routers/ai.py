from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.ai_service import GeminiService

router = APIRouter()
ai_service = GeminiService(api_key=settings.GEMINI_API_KEY)


class EnhanceRequest(BaseModel):
    content: str
    instruction: str


class GenerateRequest(BaseModel):
    prompt: str


@router.post("/enhance")
async def enhance_content(request: EnhanceRequest):
    try:
        enhanced = await ai_service.enhance(request.content, request.instruction)
        return {"enhanced_content": enhanced}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/generate")
async def generate_content(request: GenerateRequest):
    try:
        generated = await ai_service.generate(request.prompt)
        return {"content": generated}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
