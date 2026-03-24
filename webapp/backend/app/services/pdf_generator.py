from datetime import datetime
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

from app.config import settings
from app.services.layout_manager import LayoutManager


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

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
            title=title,
        )

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            "DocHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#111111"),
            spaceBefore=8,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#222222"),
            spaceAfter=4,
        )
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#111111"),
            alignment=1,
            spaceAfter=8,
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#4b5563"),
            alignment=1,
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
                        leftIndent=4,
                        value=(index + 1) if is_ordered else None,
                    )
                    for index, item in enumerate(block.get("items", []))
                ]
                bullet_type = "1" if is_ordered else "bullet"
                story.append(ListFlowable(items, bulletType=bullet_type, start="1"))
                story.append(Spacer(1, 4))

            elif b_type == "code":
                code_text = block.get("text", "")
                code_style = ParagraphStyle(
                    "DocCode",
                    parent=body_style,
                    fontName="Courier",
                    fontSize=9.5,
                    leading=12,
                    backColor=colors.HexColor("#f3f4f6"),
                    leftIndent=4,
                    rightIndent=4,
                    spaceAfter=6,
                )
                story.append(Preformatted(code_text, code_style))

            elif b_type == "hr":
                story.append(
                    HRFlowable(color=colors.HexColor("#9ca3af"), thickness=0.8)
                )
                story.append(Spacer(1, 8))

        doc.build(story)
        return output_path
