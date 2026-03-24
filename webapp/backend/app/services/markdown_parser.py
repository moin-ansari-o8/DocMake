from html import escape
from typing import Any

from markdown_it import MarkdownIt


InlineTokens = list


class MarkdownParser:
    def __init__(self) -> None:
        self.md = (
            MarkdownIt("commonmark", {"breaks": True})
            .enable("table")
            .enable("strikethrough")
        )
        for rule in ("sub", "sup"):
            try:
                self.md.enable(rule)
            except ValueError:
                # markdown-it-py may not ship optional sub/sup plugins; skip quietly
                continue

    def _inline_to_html(self, tokens: InlineTokens) -> str:
        parts: list[str] = []
        for tok in tokens:
            if tok.type == "text":
                parts.append(escape(tok.content))
            elif tok.type in {"softbreak", "hardbreak"}:
                parts.append("<br/>")
            elif tok.type in {"strong_open", "strong_close"}:
                parts.append("<b>" if tok.nesting == 1 else "</b>")
            elif tok.type in {"em_open", "em_close"}:
                parts.append("<i>" if tok.nesting == 1 else "</i>")
            elif tok.type in {"s_open", "s_close"}:
                parts.append("<strike>" if tok.nesting == 1 else "</strike>")
            elif tok.type in {"sub_open", "sub_close"}:
                parts.append("<sub>" if tok.nesting == 1 else "</sub>")
            elif tok.type in {"sup_open", "sup_close"}:
                parts.append("<sup>" if tok.nesting == 1 else "</sup>")
            elif tok.type == "code_inline":
                parts.append(f"<code>{escape(tok.content)}</code>")
            elif tok.type == "link_open":
                attrs = tok.attrs or {}
                if isinstance(attrs, dict):
                    href = attrs.get("href", "#")
                else:
                    href = next((attr[1] for attr in attrs if attr[0] == "href"), "#")
                parts.append(f'<a href="{escape(href)}">')
            elif tok.type == "link_close":
                parts.append("</a>")
        return "".join(parts)

    def parse(self, content: str) -> dict[str, Any]:
        tokens = self.md.parse(content or "")
        blocks: list[dict[str, Any]] = []
        title: str | None = None
        subtitle: str | None = None

        i = 0
        while i < len(tokens):
            tok = tokens[i]

            if tok.type == "heading_open":
                level = int(tok.tag[-1]) if tok.tag and tok.tag.startswith("h") else 1
                inline = tokens[i + 1]
                text = (
                    self._inline_to_html(inline.children or [])
                    if inline.type == "inline"
                    else ""
                )
                if level == 1 and title is None:
                    title = self._strip_tags(text)
                else:
                    blocks.append({"type": "heading", "level": level, "text": text})
                i += 2
                continue

            if tok.type == "blockquote_open":
                # treat first blockquote as subtitle, others as paragraphs
                inner = tokens[i + 1] if i + 1 < len(tokens) else None
                if inner and inner.type == "paragraph_open":
                    inline = tokens[i + 2]
                    text = (
                        self._inline_to_html(inline.children or [])
                        if inline.type == "inline"
                        else ""
                    )
                    if subtitle is None:
                        subtitle = self._strip_tags(text)
                    else:
                        blocks.append({"type": "paragraph", "text": text})
                i += 4  # blockquote_open, paragraph_open, inline, paragraph_close, blockquote_close
                continue

            if tok.type == "paragraph_open":
                inline = tokens[i + 1]
                html_text = (
                    self._inline_to_html(inline.children or [])
                    if inline.type == "inline"
                    else ""
                )
                blocks.append({"type": "paragraph", "text": html_text})
                i += 3
                continue

            if tok.type in {"bullet_list_open", "ordered_list_open"}:
                items: list[str] = []
                i += 1
                while (
                    i < len(tokens)
                    and tokens[i].type != "bullet_list_close"
                    and tokens[i].type != "ordered_list_close"
                ):
                    if tokens[i].type == "list_item_open":
                        # expect paragraph or inline inside
                        j = i + 1
                        item_parts: list[str] = []
                        while tokens[j].type != "list_item_close":
                            if tokens[j].type == "inline":
                                item_parts.append(
                                    self._inline_to_html(tokens[j].children or [])
                                )
                            j += 1
                        items.append("<br/>".join(item_parts))
                        i = j
                    i += 1
                blocks.append(
                    {
                        "type": "list",
                        "ordered": tok.type == "ordered_list_open",
                        "items": items,
                    }
                )
                i += 1
                continue

            if tok.type == "fence":
                blocks.append({"type": "code", "text": tok.content, "info": tok.info})
                i += 1
                continue

            if tok.type == "hr":
                blocks.append({"type": "hr"})
                i += 1
                continue

            i += 1

        if title is None:
            title = "Document"

        return {
            "title": title,
            "subtitle": subtitle or "",
            "blocks": blocks,
        }

    def _strip_tags(self, html: str) -> str:
        # minimal strip since we only generate simple tags
        return (
            html.replace("<b>", "")
            .replace("</b>", "")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<sub>", "")
            .replace("</sub>", "")
            .replace("<sup>", "")
            .replace("</sup>", "")
            .replace("<strike>", "")
            .replace("</strike>", "")
            .replace("<code>", "")
            .replace("</code>", "")
            .replace('<a href="#">', "")
            .replace("</a>", "")
        )
