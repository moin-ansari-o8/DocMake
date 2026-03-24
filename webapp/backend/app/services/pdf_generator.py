from datetime import datetime
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
)

from app.config import settings
from app.services.layout_manager import LayoutManager

MIN_FRAME_DIMENSION = 20


class PDFGenerator:
    def __init__(self, layout_id: str = "default"):
        manager = LayoutManager()
        self.layout = manager.get(layout_id) or manager.get("default")

    def _safe_filename(self, title: str) -> str:
        slug = (
            re.sub(r"[^a-zA-Z0-9]+", "_", title.strip().lower()).strip("_")
            or "document"
        )
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{slug}_{ts}.pdf"

    def generate(self, content: dict, title: str) -> Path:
        filename = self._safe_filename(title)
        output_path = settings.PDF_OUTPUT_DIR / filename

        config = self.layout.get("config", {})
        margins = config.get("margins", {})
        left_margin = float(margins.get("left", 12)) * mm
        right_margin = float(margins.get("right", 12)) * mm
        top_margin = float(margins.get("top", 16)) * mm
        bottom_margin = float(margins.get("bottom", 16)) * mm

        header = config.get("header", {}) or {}
        footer = config.get("footer", {}) or {}
        bars = config.get("bars", {}) or {}
        background = config.get("background", {}) or {}
        body = config.get("body", {}) or {}
        body_layout = body.get("layout", {}) or {}
        list_cfg = body.get("list", {}) or {}
        para_cfg = body.get("paragraph", {}) or {}
        code_cfg = body.get("code", {}) or {}
        hr_cfg = body.get("hr", {}) or {}
        fonts = config.get("fonts", {}) or {}
        colors_cfg = config.get("colors", {}) or {}
        title_cfg = config.get("title", {}) or {}
        subtitle_cfg = config.get("subtitle", {}) or {}

        header_h = float(header.get("height", 0)) * mm
        footer_h = float(footer.get("height", 0)) * mm
        header_pad = float(header.get("padding", 6)) * mm
        footer_pad = float(footer.get("padding", 6)) * mm

        doc = BaseDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
            title=title,
        )

        frame_y = doc.bottomMargin + footer_h
        frame_h = max(
            MIN_FRAME_DIMENSION,
            doc.height - header_h - footer_h,
        )
        columns = int(body_layout.get("columns", 1) or 1)
        gutter = float(body_layout.get("gutter", 12)) * mm
        usable_w = doc.width
        col_w = (
            usable_w
            if columns == 1
            else max((usable_w - gutter) / 2.0, MIN_FRAME_DIMENSION)
        )

        frames = [
            Frame(
                doc.leftMargin,
                frame_y,
                col_w,
                frame_h,
                id="col1",
                leftPadding=0,
                rightPadding=0,
                topPadding=0,
                bottomPadding=0,
            )
        ]
        if columns == 2:
            frames.append(
                Frame(
                    doc.leftMargin + col_w + gutter,
                    frame_y,
                    col_w,
                    frame_h,
                    id="col2",
                    leftPadding=0,
                    rightPadding=0,
                    topPadding=0,
                    bottomPadding=0,
                )
            )

        doc.addPageTemplates(
            [
                PageTemplate(
                    id="layout",
                    frames=frames,
                    onPage=lambda canvas, d: self._draw_page_decorations(
                        canvas,
                        d,
                        background=background,
                        bars=bars,
                        header=header,
                        footer=footer,
                        header_pad=header_pad,
                        footer_pad=footer_pad,
                    ),
                )
            ]
        )

        styles = getSampleStyleSheet()
        body_font = (fonts.get("body", {}) or {}).get("name", "Helvetica")
        body_size = float((fonts.get("body", {}) or {}).get("size", 10.5))
        heading_font = (fonts.get("heading", {}) or {}).get("name", "Helvetica-Bold")
        heading_size = float((fonts.get("heading", {}) or {}).get("size", 13))
        code_font = (fonts.get("code", {}) or {}).get("name", "Courier")
        code_size = float((fonts.get("code", {}) or {}).get("size", 9.5))

        paragraph_space = float(para_cfg.get("space_after", 6))
        list_indent = float(list_cfg.get("indent", 8))
        list_item_spacing = float(list_cfg.get("item_spacing", 2))
        list_bullet = str(list_cfg.get("bullet", "disc")).lower()

        body_color = colors.HexColor(colors_cfg.get("body", "#222222"))
        heading_color = colors.HexColor(colors_cfg.get("heading", "#111111"))
        border_color = colors.HexColor(colors_cfg.get("border", "#9ca3af"))

        title_align = self._alignment(title_cfg.get("align", "center"))
        subtitle_align = self._alignment(subtitle_cfg.get("align", "center"))
        title_color = colors.HexColor(title_cfg.get("color", colors_cfg.get("heading", "#111111")))
        subtitle_color = colors.HexColor(subtitle_cfg.get("color", "#4b5563"))

        heading_style = ParagraphStyle(
            "DocHeading",
            parent=styles["Heading2"],
            fontName=heading_font,
            fontSize=heading_size,
            leading=16,
            textColor=heading_color,
            spaceBefore=8,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=body_size,
            leading=14,
            textColor=body_color,
            spaceAfter=paragraph_space,
        )
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Title"],
            fontName=heading_font,
            fontSize=20,
            leading=24,
            textColor=title_color,
            alignment=title_align,
            spaceAfter=8,
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=11,
            leading=14,
            textColor=subtitle_color,
            alignment=subtitle_align,
            spaceAfter=18,
        )

        story: list = [Paragraph(content.get("title", title), title_style)]
        subtitle = content.get("subtitle", "")
        if subtitle:
            story.append(Paragraph(subtitle, subtitle_style))
        else:
            story.append(Spacer(1, 12))

        for block in content.get("blocks", []):
            b_type = block.get("type")
            if b_type == "heading":
                level = block.get("level", 2)
                style = heading_style
                if level >= 3:
                    style = ParagraphStyle(
                        f"DocHeading{level}",
                        parent=body_style,
                        fontName="Helvetica-Bold",
                        fontSize=11 if level == 3 else 10,
                        leading=14,
                        spaceBefore=6,
                        spaceAfter=4,
                    )
                story.append(Paragraph(block.get("text", ""), style))
                story.append(Spacer(1, 2))

            elif b_type == "paragraph":
                text = block.get("text", "")
                story.append(Paragraph(text, body_style))
                story.append(Spacer(1, 4))

            elif b_type == "list":
                is_ordered = bool(block.get("ordered"))
                items = [
                    ListItem(
                        Paragraph(item or "", body_style),
                        leftIndent=list_indent,
                        spaceBefore=0,
                        spaceAfter=list_item_spacing,
                        value=(index + 1) if is_ordered else None,
                    )
                    for index, item in enumerate(block.get("items", []))
                ]
                if items:
                    bullet_map = {"disc": "•", "circle": "○", "square": "▪"}
                    list_kwargs = (
                        {"bulletType": "1", "start": "1"}
                        if is_ordered
                        else {
                            "bulletType": "bullet",
                            "bulletChar": bullet_map.get(list_bullet, "•"),
                            "bulletFontName": body_font,
                            "bulletFontSize": max(body_size - 0.5, 8),
                        }
                    )
                    story.append(ListFlowable(items, **list_kwargs))
                    story.append(Spacer(1, paragraph_space))

            elif b_type == "code":
                code_text = block.get("text", "")
                code_padding = float(code_cfg.get("padding", 6))
                code_bg = colors.HexColor(code_cfg.get("bg", "#f3f4f6"))
                code_border = colors.HexColor(code_cfg.get("border", "#e5e7eb"))
                code_style = ParagraphStyle(
                    "DocCode",
                    parent=body_style,
                    fontName=code_font,
                    fontSize=code_size,
                    leading=12,
                    backColor=code_bg,
                    leftIndent=code_padding,
                    rightIndent=code_padding,
                    borderColor=code_border,
                    borderWidth=0.5,
                    borderPadding=code_padding,
                    spaceAfter=6,
                )
                story.append(Preformatted(code_text, code_style))

            elif b_type == "hr":
                hr_thickness = float(hr_cfg.get("thickness", 1))
                hr_color = colors.HexColor(hr_cfg.get("color", colors_cfg.get("border", "#9ca3af")))
                story.append(
                    HRFlowable(
                        color=hr_color,
                        thickness=hr_thickness,
                        leftIndent=0,
                        rightIndent=0,
                    )
                )
                story.append(Spacer(1, 8))

        try:
            doc.build(story)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"Failed to build PDF during doc_build "
                f"(layout={self.layout.get('id', 'unknown')}, title={title!r}): {exc}"
            ) from exc
        return output_path

    def _alignment(self, align: str) -> int:
        return {"left": 0, "center": 1, "right": 2}.get((align or "center").lower(), 1)

    def _draw_page_decorations(
        self,
        canvas,
        doc,
        *,
        background: dict,
        bars: dict,
        header: dict,
        footer: dict,
        header_pad: float,
        footer_pad: float,
    ) -> None:
        width, height = doc.pagesize

        bg_color = background.get("color")
        if bg_color:
            canvas.saveState()
            canvas.setFillColor(colors.HexColor(bg_color))
            canvas.rect(0, 0, width, height, stroke=0, fill=1)
            canvas.restoreState()

        bg_image = background.get("image")
        if bg_image:
            self._draw_background_image(canvas, width, height, bg_image, str(background.get("mode", "cover")))

        top = bars.get("top") or {}
        bottom = bars.get("bottom") or {}
        top_h = float(top.get("height", 0)) * mm
        bottom_h = float(bottom.get("height", 0)) * mm
        if top_h > 0:
            canvas.saveState()
            canvas.setFillColor(colors.HexColor(top.get("color", "#111111")))
            canvas.rect(0, height - top_h, width, top_h, stroke=0, fill=1)
            canvas.restoreState()
        if bottom_h > 0:
            canvas.saveState()
            canvas.setFillColor(colors.HexColor(bottom.get("color", "#9ca3af")))
            canvas.rect(0, 0, width, bottom_h, stroke=0, fill=1)
            canvas.restoreState()

        self._draw_header_footer(
            canvas,
            doc,
            header=header,
            footer=footer,
            header_pad=header_pad,
            footer_pad=footer_pad,
        )

    def _draw_header_footer(self, canvas, doc, *, header: dict, footer: dict, header_pad: float, footer_pad: float) -> None:
        width, height = doc.pagesize
        left_x = doc.leftMargin
        right_x = width - doc.rightMargin
        center_x = (left_x + right_x) / 2.0

        self._draw_hf_block(
            canvas,
            base_y=height - doc.topMargin,
            cfg=header,
            pad=header_pad,
            left_x=left_x,
            center_x=center_x,
            right_x=right_x,
            top_anchor=True,
        )
        self._draw_hf_block(
            canvas,
            base_y=doc.bottomMargin,
            cfg=footer,
            pad=footer_pad,
            left_x=left_x,
            center_x=center_x,
            right_x=right_x,
            top_anchor=False,
        )

    def _draw_hf_block(
        self,
        canvas,
        *,
        base_y: float,
        cfg: dict,
        pad: float,
        left_x: float,
        center_x: float,
        right_x: float,
        top_anchor: bool,
    ) -> None:
        h = float(cfg.get("height", 0)) * mm
        if h <= 0:
            return
        text = (cfg.get("text") or "").strip()
        logo = (cfg.get("logo") or "").strip()
        align = str(cfg.get("align", "center")).lower()
        color = colors.HexColor(cfg.get("color", "#111111"))
        text_y = base_y - (pad + 8) if top_anchor else base_y + pad + 2

        if logo:
            try:
                logo_norm = logo.lstrip("/")
                if logo_norm.startswith("assets/"):
                    logo_norm = logo_norm[len("assets/") :]
                logo_path = (settings.ASSETS_DIR / logo_norm).resolve()
                logo_path.relative_to(settings.ASSETS_DIR.resolve())
                if logo_path.exists():
                    img = ImageReader(str(logo_path))
                    img_w = min(24 * mm, 0.8 * h)
                    img_h = min(24 * mm, 0.8 * h)
                    x = self._resolve_aligned_x(align, left_x, center_x, right_x, img_w)
                    y = base_y - h + pad if top_anchor else base_y + pad
                    canvas.drawImage(img, x, y, width=img_w, height=img_h, preserveAspectRatio=True, mask="auto")
            except Exception:  # noqa: BLE001
                pass

        if text:
            canvas.saveState()
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(color)
            if align == "left":
                canvas.drawString(left_x, text_y, text)
            elif align == "right":
                canvas.drawRightString(right_x, text_y, text)
            else:
                canvas.drawCentredString(center_x, text_y, text)
            canvas.restoreState()

    def _resolve_aligned_x(self, align: str, left_x: float, center_x: float, right_x: float, width: float) -> float:
        if align == "left":
            return left_x
        if align == "right":
            return right_x - width
        return center_x - (width / 2.0)

    def _draw_background_image(self, canvas, page_w: float, page_h: float, rel_path: str, mode: str) -> None:
        try:
            normalized = rel_path.lstrip("/")
            if normalized.startswith("assets/"):
                normalized = normalized[len("assets/") :]
            bg_path = (settings.ASSETS_DIR / normalized).resolve()
            bg_path.relative_to(settings.ASSETS_DIR.resolve())
            if not bg_path.exists():
                return
            img = ImageReader(str(bg_path))
            img_w, img_h = img.getSize()
            if img_w <= 0 or img_h <= 0:
                return
            if mode == "tile":
                tile_w = min(img_w, page_w / 3)
                tile_h = tile_w * (img_h / img_w)
                y = 0.0
                while y < page_h:
                    x = 0.0
                    while x < page_w:
                        canvas.drawImage(img, x, y, width=tile_w, height=tile_h, preserveAspectRatio=True, mask="auto")
                        x += tile_w
                    y += tile_h
                return

            page_ratio = page_w / page_h
            img_ratio = img_w / img_h
            if mode == "contain":
                if img_ratio > page_ratio:
                    w = page_w
                    h = page_w / img_ratio
                else:
                    h = page_h
                    w = page_h * img_ratio
            else:  # cover
                if img_ratio > page_ratio:
                    h = page_h
                    w = page_h * img_ratio
                else:
                    w = page_w
                    h = page_w / img_ratio
            x = (page_w - w) / 2.0
            y = (page_h - h) / 2.0
            canvas.drawImage(img, x, y, width=w, height=h, preserveAspectRatio=True, mask="auto")
        except Exception:  # noqa: BLE001
            return
