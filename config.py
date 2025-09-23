import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    UPLOAD_DIR = "uploads"
    OUTPUT_DIR = "outputs"
    # API Configuration
    API_TITLE = "Business Card OCR API"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = "Extract business card information and generate vCards"
    # Gemini LLM (Google) Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # from your .env, or set here directly

config = Config()
