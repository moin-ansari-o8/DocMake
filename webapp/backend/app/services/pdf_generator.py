from datetime import datetime
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

from app.config import settings
from app.services.layout_manager import LayoutManager


class PDFGenerator:
    def __init__(self, layout_id: str = "default"):
        manager = LayoutManager()
        self.layout = manager.get(layout_id) or manager.get("default")

    def _safe_filename(self, title: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip().lower()).strip("_") or "document"
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

        story = [
            Paragraph(content.get("title", title), title_style),
        ]
        subtitle = content.get("subtitle", "")
        if subtitle:
            story.append(Paragraph(subtitle, subtitle_style))
        else:
            story.append(Spacer(1, 12))

        for section in content.get("sections", []):
            story.append(Paragraph(section.get("heading", "Section"), heading_style))

            body_text = section.get("content", "").replace("—", ", ").replace("--", ", ")
            if body_text:
                for para in [p.strip() for p in body_text.split("\n\n") if p.strip()]:
                    story.append(Paragraph(para, body_style))
                    story.append(Spacer(1, 4))

            for sub in section.get("subsections", []):
                story.append(Paragraph(sub.get("heading", "Subsection"), heading_style))
                sub_content = sub.get("content", "").strip()
                if sub_content:
                    story.append(Paragraph(sub_content, body_style))

            story.append(Spacer(1, 6))
            story.append(HRFlowable(color=colors.HexColor("#9ca3af"), thickness=0.8))
            story.append(Spacer(1, 8))

        doc.build(story)
        return output_path
