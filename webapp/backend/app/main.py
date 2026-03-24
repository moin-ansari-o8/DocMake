from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import ai, layouts, pdf

app = FastAPI(
    title="DocMake API",
    version="1.0.0",
    description="API for markdown-based PDF generation with layout and AI services",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf.router, prefix="/api/pdf", tags=["PDF"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(layouts.router, prefix="/api/layouts", tags=["Layouts"])

app.mount("/pdf-output", StaticFiles(directory=str(settings.PDF_OUTPUT_DIR)), name="pdf-output")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "DocMake API", "status": "running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
