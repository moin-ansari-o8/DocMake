from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.layout_manager import LayoutManager

router = APIRouter()
layout_manager = LayoutManager()


class LayoutBase(BaseModel):
    name: str
    description: str | None = ""
    config: dict[str, Any]
    base: str | None = None
    version: int | None = None


class LayoutUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    version: int | None = None


class LayoutCloneRequest(BaseModel):
    source_id: str
    name: str | None = None
    description: str | None = None


@router.get("")
async def list_layouts():
    return layout_manager.list_all()


@router.get("/{layout_id}")
async def get_layout(layout_id: str):
    layout = layout_manager.get(layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    return layout


@router.post("/clone")
async def clone_layout(body: LayoutCloneRequest):
    try:
        return layout_manager.clone(
            body.source_id, name=body.name, description=body.description
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("")
async def create_layout(layout: LayoutBase):
    try:
        return layout_manager.create(layout.model_dump(exclude_unset=True))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{layout_id}")
async def update_layout(layout_id: str, layout: LayoutUpdate):
    try:
        updated = layout_manager.update(
            layout_id, layout.model_dump(exclude_unset=True)
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail="Layout not found or immutable")
    return updated


@router.delete("/{layout_id}")
async def delete_layout(layout_id: str):
    success = layout_manager.delete(layout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Layout not found or immutable")
    return {"message": "Layout deleted"}
