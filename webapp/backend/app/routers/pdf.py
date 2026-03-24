from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.markdown_parser import MarkdownParser
from app.services.pdf_generator import PDFGenerator

router = APIRouter()


class GeneratePDFRequest(BaseModel):
    content: str
    layout_id: str = "default"
    title: str = "Document"


class PreflightResponse(BaseModel):
    valid: bool
    title: str
    subtitle: str
    blocks: list[dict]
    warnings: list[str] = []


def _build_warnings(parsed: dict) -> list[str]:
    warnings: list[str] = []
    for block in parsed.get("blocks", []):
        if block.get("type") == "list" and not block.get("items"):
            warnings.append("List contained no valid items after normalization.")
    return warnings


@router.post("/generate")
async def generate_pdf(request: GeneratePDFRequest):
    try:
        parser = MarkdownParser()
        parsed = parser.parse(request.content)

        generator = PDFGenerator(layout_id=request.layout_id)
        output_path = generator.generate(content=parsed, title=request.title)

        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename=f"{request.title}.pdf",
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail={
                "error": "pdf_generation_failed",
                "message": str(exc),
                "layout_id": request.layout_id,
            },
        ) from exc


@router.post("/preflight", response_model=PreflightResponse)
async def preflight_pdf(request: GeneratePDFRequest):
    try:
        parser = MarkdownParser()
        parsed = parser.parse(request.content)
        return PreflightResponse(
            valid=True,
            title=parsed.get("title", ""),
            subtitle=parsed.get("subtitle", ""),
            blocks=parsed.get("blocks", []),
            warnings=_build_warnings(parsed),
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail={"error": "preflight_failed", "message": str(exc)},
        ) from exc


@router.post("/preview")
async def preview_pdf(request: GeneratePDFRequest):
    return await generate_pdf(request)
