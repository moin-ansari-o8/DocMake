from imghdr import what as detect_image_type
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import settings

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {
    "logo": {".png", ".jpg", ".jpeg", ".svg"},
    "background": {".png", ".jpg", ".jpeg"},
}
ALLOWED_MIME_TYPES = {
    "logo": {"image/png", "image/jpeg", "image/svg+xml"},
    "background": {"image/png", "image/jpeg"},
}


@router.post("/upload")
async def upload_asset(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    kind: str = Form(...),  # logo | background
):
    normalized_kind = (kind or "").strip().lower()
    if normalized_kind not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid asset kind")

    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS[normalized_kind]:
        raise HTTPException(status_code=400, detail="File extension not allowed")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty upload")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_MIME_TYPES[normalized_kind]:
        raise HTTPException(status_code=400, detail="MIME type not allowed")

    if content_type != "image/svg+xml":
        detected = detect_image_type(None, h=content)
        if detected not in {"png", "jpeg"}:
            raise HTTPException(status_code=400, detail="Invalid image content")

    safe_user = "".join(ch for ch in user_id if ch.isalnum() or ch in {"-", "_"})
    if not safe_user:
        raise HTTPException(status_code=400, detail="Invalid user id")

    user_dir = settings.ASSETS_DIR / safe_user
    user_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{normalized_kind}_{uuid4().hex[:10]}{ext}"
    path = user_dir / filename
    path.write_bytes(content)

    rel = path.relative_to(settings.ASSETS_DIR).as_posix()
    return {"path": rel, "kind": normalized_kind, "size": len(content)}
