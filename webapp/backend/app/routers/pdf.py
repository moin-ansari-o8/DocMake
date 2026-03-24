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
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/preview")
async def preview_pdf(request: GeneratePDFRequest):
    return await generate_pdf(request)
