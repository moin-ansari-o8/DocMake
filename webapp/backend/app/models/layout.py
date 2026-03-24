from __future__ import annotations

from pathlib import PurePosixPath
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, root_validator, validator


class Margins(BaseModel):
    left: float = Field(12, ge=0)
    right: float = Field(12, ge=0)
    top: float = Field(16, ge=0)
    bottom: float = Field(16, ge=0)


class FontSpec(BaseModel):
    name: str = Field("Helvetica")
    size: float = Field(10.5, gt=0)


class Fonts(BaseModel):
    body: FontSpec = Field(default_factory=FontSpec)
    heading: FontSpec = Field(
        default_factory=lambda: FontSpec(name="Helvetica-Bold", size=13)
    )
    code: FontSpec = Field(default_factory=lambda: FontSpec(name="Courier", size=9.5))


class Colors(BaseModel):
    body: str = "#222222"
    heading: str = "#111111"
    border: str = "#9ca3af"


class Palette(BaseModel):
    primary: str | None = None
    muted: str | None = None
    surface: str | None = None


class TitleStyle(BaseModel):
    align: str = Field("center", pattern="^(left|center|right)$")
    color: str | None = None


class SubtitleStyle(BaseModel):
    align: str = Field("center", pattern="^(left|center|right)$")
    color: str | None = None


class ParagraphStyleConfig(BaseModel):
    space_after: float = Field(6, ge=0)


class ListStyleConfig(BaseModel):
    indent: float = Field(8, ge=0)
    item_spacing: float = Field(2, ge=0)
    bullet: str = Field("disc")


class CodeStyleConfig(BaseModel):
    padding: float = Field(6, ge=0)
    bg: str = "#f3f4f6"
    border: str | None = "#e5e7eb"


class HrStyleConfig(BaseModel):
    thickness: float = Field(1, ge=0)
    color: str = "#9ca3af"


class BodyLayout(BaseModel):
    columns: int = Field(1, ge=1, le=2)
    gutter: float = Field(12, ge=0)


class BodyConfig(BaseModel):
    paragraph: ParagraphStyleConfig = Field(default_factory=ParagraphStyleConfig)
    list: ListStyleConfig = Field(default_factory=ListStyleConfig)
    code: CodeStyleConfig = Field(default_factory=CodeStyleConfig)
    hr: HrStyleConfig = Field(default_factory=HrStyleConfig)
    layout: BodyLayout = Field(default_factory=BodyLayout)


class HeaderFooterConfig(BaseModel):
    height: float = Field(0, ge=0)
    padding: float = Field(6, ge=0)
    text: str | None = None
    logo: str | None = None
    align: str = Field("center", pattern="^(left|center|right)$")
    color: str | None = None

    @validator("logo")
    def _validate_logo(cls, v: Optional[str]) -> Optional[str]:  # noqa: N805
        return _validate_asset_path(v)


class BarSpec(BaseModel):
    height: float = Field(0, ge=0)
    color: str = "#111111"


class BarsConfig(BaseModel):
    top: BarSpec = Field(default_factory=BarSpec)
    bottom: BarSpec = Field(default_factory=lambda: BarSpec(color="#9ca3af"))


class BackgroundConfig(BaseModel):
    color: str | None = "#ffffff"
    image: str | None = None
    mode: str = Field("cover", pattern="^(cover|contain|tile)$")

    @validator("image")
    def _validate_image(cls, v: Optional[str]) -> Optional[str]:  # noqa: N805
        return _validate_asset_path(v)


class LayoutConfig(BaseModel):
    margins: Margins = Field(default_factory=Margins)
    fonts: Fonts = Field(default_factory=Fonts)
    colors: Colors = Field(default_factory=Colors)
    palette: Palette = Field(default_factory=Palette)
    title: TitleStyle = Field(default_factory=TitleStyle)
    subtitle: SubtitleStyle = Field(default_factory=SubtitleStyle)
    body: BodyConfig = Field(default_factory=BodyConfig)
    header: HeaderFooterConfig = Field(default_factory=HeaderFooterConfig)
    footer: HeaderFooterConfig = Field(default_factory=HeaderFooterConfig)
    bars: BarsConfig = Field(default_factory=BarsConfig)
    background: BackgroundConfig = Field(default_factory=BackgroundConfig)


class Layout(BaseModel):
    id: str | None = None
    name: str
    description: str | None = ""
    version: int = 1
    base: str | None = None
    config: LayoutConfig = Field(default_factory=LayoutConfig)
    immutable: bool = False

    @root_validator(pre=True)
    def _assign_id(cls, values: dict) -> dict:  # noqa: N805
        if not values.get("id"):
            values["id"] = str(uuid4())[:8]
        return values

    @validator("version")
    def _validate_version(cls, v: int) -> int:  # noqa: N805
        if v < 1:
            raise ValueError("version must be >= 1")
        return v


def _validate_asset_path(path: Optional[str]) -> Optional[str]:
    if path is None or path == "":
        return None
    p = PurePosixPath(path)
    if p.is_absolute():
        raise ValueError("asset paths must be relative")
    if any(part == ".." for part in p.parts):
        raise ValueError("asset paths cannot traverse directories")
    return str(p)
