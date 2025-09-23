import os
import logging
from typing import Optional
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    """Service class for handling OCR operations with RapidOCR"""

    def __init__(self):
        # Initialize RapidOCR model
        self.ocr = RapidOCR()

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize if too small (similar to your old logic)
            width, height = image.size
            if width < 1000 or height < 1000:
                scale_factor = max(1000/width, 1000/height)
                new_size = (int(width * scale_factor), int(height * scale_factor))
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            return image

        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image

    def extract_text_from_image(self, image: Image.Image) -> Optional[str]:
        """Extract text from image using RapidOCR"""
        try:
            processed_image = self.preprocess_image(image)

            # Run OCR
            result, _ = self.ocr(processed_image)

            if not result:
                logger.warning("No text detected by RapidOCR")
                return ""

            # Join recognized text lines
            text_lines = [line[1] for line in result]  # Each line: [box, text, confidence]
            text = "\n".join(text_lines)

            text = self._clean_ocr_text(text)
            logger.info(f"Successfully extracted {len(text)} characters from image")
            return text

        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            return None

    def _clean_ocr_text(self, text: str) -> str:
        """Clean OCR text by removing excessive whitespace"""
        if not text:
            return ""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)

    def save_ocr_result(self, text: str, filename: str) -> str:
        """Save OCR text result to file"""
        try:
            os.makedirs(config.OUTPUT_DIR, exist_ok=True)
            filepath = os.path.join(config.OUTPUT_DIR, f"{filename}_ocr.txt")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)

            logger.info(f"OCR result saved to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save OCR result: {str(e)}")
            raise

# Singleton instance
ocr_service = OCRService()
