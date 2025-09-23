import os
import uuid
import logging
import csv
import io

from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse,  StreamingResponse
from fastapi.staticfiles import StaticFiles

from PIL import Image

from config import config
from models import OCRResponse, BusinessCardData
from ocr_service import ocr_service
from parser_service import parser_service
from vcard_service import vcard_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description=config.API_DESCRIPTION,
)

os.makedirs(config.UPLOAD_DIR, exist_ok=True)
os.makedirs(config.OUTPUT_DIR, exist_ok=True)

# Mount static directory for serving CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

session_storage = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the frontend HTML file
    index_path = Path("static") / "index.html"
    return index_path.read_text(encoding="utf-8")

@app.post("/process-cards", response_model=OCRResponse)
async def process_business_cards(
    files: List[UploadFile] = File(..., description="Upload 1 or 2 business card images (front and back)"),
    session_id: str = Form(...),
    include_vcard: bool = Form(True),
    include_raw_text: bool = Form(True),
):
    # 1. Validate for 1 or 2 files
    if not 1 <= len(files) <= 2:
        raise HTTPException(status_code=400, detail="You must upload 1 or 2 images.")

    all_text_parts = []
    
    # 2. Perform OCR on all images and collect the text
    for file in files:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in config.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}.")

        unique_id = str(uuid.uuid4())
        filepath = os.path.join(config.UPLOAD_DIR, f"{unique_id}{file_ext}")

        try:
            with open(filepath, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            image = Image.open(filepath)
            raw_text = ocr_service.extract_text_from_image(image)
            if raw_text:
                all_text_parts.append(raw_text)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    if not all_text_parts:
        return OCRResponse(success=False, raw_text="", error_message="Failed to extract any text from the image(s).")
    
    # 3. Combine text from front and back, separated for clarity
    combined_text = "\n\n--- CARD SEPARATOR ---\n\n".join(all_text_parts)

    # 4. Parse the single combined text block
    structured_data = parser_service.extract_business_card_data(combined_text)
    if not structured_data:
        return OCRResponse(
            success=False,
            raw_text=combined_text,
            error_message="Failed to parse business card data from the combined text."
        )
        
    if session_id not in session_storage:
        session_storage[session_id] = []
    session_storage[session_id].append(structured_data)
    logger.info(f"Stored card for session {session_id}. Total cards in session: {len(session_storage[session_id])}")

    # 5. Generate a single vCard from the final structured data
    vcard_content = vcard_service.generate_vcard(structured_data) if include_vcard else None

    # 6. Return a SINGLE response object
    return OCRResponse(
        success=True,
        raw_text=combined_text if include_raw_text else "",
        structured_data=structured_data,
        vcard=vcard_content,
    )

# ✅ NEW: Add a new endpoint for exporting the CSV
@app.post("/export-csv")
async def export_csv(session_id: str = Form(...)):
    if session_id not in session_storage or not session_storage[session_id]:
        raise HTTPException(status_code=404, detail="No data available for export for this session.")

    # Get data from storage
    cards_data = [card.model_dump() for card in session_storage[session_id]]
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=BusinessCardData.model_fields.keys(), quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(cards_data)
    
    # Clear the session data after preparing the file
    del session_storage[session_id]
    logger.info(f"Cleared session data for {session_id} after export.")
    
    # Create a streaming response to send the file
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=business_cards_{uuid.uuid4().hex[:8]}.csv"}
    )