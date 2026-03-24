import json
from pathlib import Path
from typing import Any
import uuid

from app.config import settings


class LayoutManager:
    def __init__(self):
        self.layouts_dir = settings.LAYOUTS_DIR
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        defaults = {
            "default": {
                "id": "default",
                "name": "Default",
                "description": "Balanced monochrome layout",
                "config": {
                    "margins": {"left": 12, "right": 12, "top": 16, "bottom": 16},
                    "fonts": {
                        "body": {"name": "Helvetica", "size": 10.5},
                        "heading": {"name": "Helvetica-Bold", "size": 13},
                    },
                    "colors": {"body": "#222222", "heading": "#111111", "border": "#9ca3af"},
                },
            },
            "academic": {
                "id": "academic",
                "name": "Academic",
                "description": "Formal document layout",
                "config": {
                    "margins": {"left": 18, "right": 18, "top": 20, "bottom": 20},
                    "fonts": {
                        "body": {"name": "Times-Roman", "size": 11},
                        "heading": {"name": "Times-Bold", "size": 14},
                    },
                    "colors": {"body": "#1f2937", "heading": "#111111", "border": "#6b7280"},
                },
            },
            "religious": {
                "id": "religious",
                "name": "Religious",
                "description": "Traditional and clean layout",
                "config": {
                    "margins": {"left": 15, "right": 15, "top": 18, "bottom": 18},
                    "fonts": {
                        "body": {"name": "Helvetica", "size": 11},
                        "heading": {"name": "Helvetica-Bold", "size": 14},
                    },
                    "colors": {"body": "#374151", "heading": "#111111", "border": "#9ca3af"},
                },
            },
        }

        for layout_id, payload in defaults.items():
            path = self.layouts_dir / f"{layout_id}.json"
            if not path.exists():
                self._save(path, payload)

    def _load(self, path: Path) -> dict[str, Any] | None:
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            return None

    def _save(self, path: Path, layout: dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(layout, f, indent=2)

    def list_all(self) -> list[dict[str, Any]]:
        layouts = []
        for file in self.layouts_dir.glob("*.json"):
            layout = self._load(file)
            if layout:
                layouts.append(
                    {
                        "id": layout.get("id", file.stem),
                        "name": layout.get("name", file.stem),
                        "description": layout.get("description", ""),
                    }
                )
        return sorted(layouts, key=lambda item: item["name"].lower())

    def get(self, layout_id: str) -> dict[str, Any] | None:
        return self._load(self.layouts_dir / f"{layout_id}.json")

    def create(self, layout: dict[str, Any]) -> dict[str, Any]:
        layout_id = str(uuid.uuid4())[:8]
        layout["id"] = layout_id
        self._save(self.layouts_dir / f"{layout_id}.json", layout)
        return layout

    def update(self, layout_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        path = self.layouts_dir / f"{layout_id}.json"
        layout = self._load(path)
        if not layout:
            return None

        layout.update(updates)
        self._save(path, layout)
        return layout

    def delete(self, layout_id: str) -> bool:
        if layout_id in {"default", "academic", "religious"}:
            return False

        path = self.layouts_dir / f"{layout_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False
