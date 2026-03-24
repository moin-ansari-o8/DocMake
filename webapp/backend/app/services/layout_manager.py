import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import ValidationError

from app.config import settings
from app.models.layout import Layout


class LayoutManager:
    def __init__(self):
        self.layouts_dir = settings.LAYOUTS_DIR
        self.assets_dir = settings.ASSETS_DIR
        self.default_ids = {"default", "academic", "religious"}
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        defaults = {
            "default": {
                "id": "default",
                "name": "Default",
                "description": "Balanced monochrome layout",
                "immutable": True,
                "config": {
                    "margins": {"left": 12, "right": 12, "top": 16, "bottom": 16},
                    "fonts": {
                        "body": {"name": "Helvetica", "size": 10.5},
                        "heading": {"name": "Helvetica-Bold", "size": 13},
                    },
                    "colors": {
                        "body": "#222222",
                        "heading": "#111111",
                        "border": "#9ca3af",
                    },
                },
            },
            "academic": {
                "id": "academic",
                "name": "Academic",
                "description": "Formal document layout",
                "immutable": True,
                "config": {
                    "margins": {"left": 18, "right": 18, "top": 20, "bottom": 20},
                    "fonts": {
                        "body": {"name": "Times-Roman", "size": 11},
                        "heading": {"name": "Times-Bold", "size": 14},
                    },
                    "colors": {
                        "body": "#1f2937",
                        "heading": "#111111",
                        "border": "#6b7280",
                    },
                },
            },
            "religious": {
                "id": "religious",
                "name": "Religious",
                "description": "Traditional and clean layout",
                "immutable": True,
                "config": {
                    "margins": {"left": 15, "right": 15, "top": 18, "bottom": 18},
                    "fonts": {
                        "body": {"name": "Helvetica", "size": 11},
                        "heading": {"name": "Helvetica-Bold", "size": 14},
                    },
                    "colors": {
                        "body": "#374151",
                        "heading": "#111111",
                        "border": "#9ca3af",
                    },
                },
            },
        }

        for layout_id, payload in defaults.items():
            path = self.layouts_dir / f"{layout_id}.json"
            if not path.exists():
                validated = Layout(**payload).dict()
                self._save(path, validated)

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
                        "immutable": bool(layout.get("immutable", False)),
                    }
                )
        return sorted(layouts, key=lambda item: item["name"].lower())

    def get(self, layout_id: str) -> dict[str, Any] | None:
        return self._load(self.layouts_dir / f"{layout_id}.json")

    def clone(
        self, source_id: str, name: str | None = None, description: str | None = None
    ) -> dict[str, Any]:
        source = self.get(source_id)
        if not source:
            raise ValueError("Layout not found")
        clone_payload = {
            "id": str(uuid4())[:8],
            "name": name or f"{source.get('name', source_id)} Copy",
            "description": description or source.get("description", ""),
            "base": source.get("id", source_id),
            "config": source.get("config", {}),
            "version": 1,
            "immutable": False,
        }
        validated = self._validate_payload(clone_payload)
        self._save(self.layouts_dir / f"{validated['id']}.json", validated)
        return validated

    def create(self, layout: dict[str, Any]) -> dict[str, Any]:
        validated = self._validate_payload(layout)
        self._save(self.layouts_dir / f"{validated['id']}.json", validated)
        return validated

    def update(self, layout_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        path = self.layouts_dir / f"{layout_id}.json"
        layout = self._load(path)
        if not layout:
            return None
        if layout.get("immutable") or layout_id in self.default_ids:
            return None

        merged = {**layout, **updates}
        merged["id"] = layout_id
        merged["version"] = int(layout.get("version", 1)) + 1
        merged["immutable"] = False

        validated = self._validate_payload(merged)
        self._save(path, validated)
        return validated

    def delete(self, layout_id: str) -> bool:
        if layout_id in self.default_ids:
            return False

        path = self.layouts_dir / f"{layout_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    def _validate_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            model = Layout(**payload)
        except ValidationError as exc:
            raise ValueError(exc.errors()) from exc
        data = model.dict()
        self._validate_asset_references(data)
        return data

    def _validate_asset_references(self, layout: dict[str, Any]) -> None:
        config = layout.get("config", {})
        header_logo = (((config.get("header") or {}).get("logo")) or "").strip()
        footer_logo = (((config.get("footer") or {}).get("logo")) or "").strip()
        bg_image = (((config.get("background") or {}).get("image")) or "").strip()

        for rel_path in [header_logo, footer_logo, bg_image]:
            if not rel_path:
                continue
            resolved = (self.assets_dir / rel_path).resolve()
            try:
                resolved.relative_to(self.assets_dir.resolve())
            except ValueError as exc:
                raise ValueError("Asset path escapes assets root") from exc
            if not resolved.exists():
                raise ValueError(f"Asset not found: {rel_path}")
