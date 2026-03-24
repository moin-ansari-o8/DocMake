from typing import Any


class MarkdownParser:
    def parse(self, content: str) -> dict[str, Any]:
        lines = content.strip().split("\n") if content.strip() else []

        document: dict[str, Any] = {
            "title": "",
            "subtitle": "",
            "sections": [],
        }

        current_section = None
        current_content: list[str] = []

        for line in lines:
            if line.startswith("# "):
                document["title"] = line[2:].strip()
            elif line.startswith("> ") and current_section is None:
                document["subtitle"] = line[2:].strip()
            elif line.startswith("## "):
                if current_section:
                    current_section["content"] = "\n".join(current_content).strip()
                    document["sections"].append(current_section)

                current_section = {
                    "heading": line[3:].strip(),
                    "subsections": [],
                    "content": "",
                }
                current_content = []
            elif line.startswith("### "):
                if current_section:
                    current_section["subsections"].append(
                        {"heading": line[4:].strip(), "content": ""}
                    )
            else:
                current_content.append(line)

        if current_section:
            current_section["content"] = "\n".join(current_content).strip()
            document["sections"].append(current_section)

        if not document["title"]:
            document["title"] = "Document"

        return document
