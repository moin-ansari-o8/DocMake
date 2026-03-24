from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    PDF_OUTPUT_DIR: Path = BASE_DIR / "pdf-output"
    LAYOUTS_DIR: Path = BASE_DIR / "layouts"
    ASSETS_DIR: Path = BASE_DIR / "assets"

    GEMINI_API_KEY: str = ""

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
settings.PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.LAYOUTS_DIR.mkdir(parents=True, exist_ok=True)
settings.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
