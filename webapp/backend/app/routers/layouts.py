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


class LayoutUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


@router.get("")
async def list_layouts():
    return layout_manager.list_all()


@router.get("/{layout_id}")
async def get_layout(layout_id: str):
    layout = layout_manager.get(layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    return layout


@router.post("")
async def create_layout(layout: LayoutBase):
    return layout_manager.create(layout.model_dump())


@router.put("/{layout_id}")
async def update_layout(layout_id: str, layout: LayoutUpdate):
    updated = layout_manager.update(layout_id, layout.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Layout not found")
    return updated


@router.delete("/{layout_id}")
async def delete_layout(layout_id: str):
    success = layout_manager.delete(layout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Layout not found")
    return {"message": "Layout deleted"}
