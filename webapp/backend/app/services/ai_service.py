import google.generativeai as genai


class GeminiService:
    def __init__(self, api_key: str):
        self.model = None
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def enhance(self, content: str, instruction: str) -> str:
        if not self.model:
            raise ValueError("Gemini API key not configured")

        prompt = f"""You are a professional content editor.

INSTRUCTION: {instruction}

CONTENT TO ENHANCE:
{content}

Respond with ONLY the enhanced markdown content.
Use clear formatting and professional tone.
Do not use em dashes (—) or double hyphens (--).
"""
        response = await self.model.generate_content_async(prompt)
        return response.text

    async def generate(self, prompt: str) -> str:
        if not self.model:
            raise ValueError("Gemini API key not configured")

        system_prompt = f"""You are a professional writer.

USER REQUEST: {prompt}

Generate structured markdown with headings and concise paragraphs.
Do not use em dashes (—) or double hyphens (--).
"""
        response = await self.model.generate_content_async(system_prompt)
        return response.text
