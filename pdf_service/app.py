import tempfile
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pdf_service.pdf_text import extract_text_from_pdf as extract_text_base
from pdf_service.ocr import ocr_pdf
from pdf_service.models import ExtractedTextResponse

app = FastAPI(title="PDF Extraction Service")


@app.post("/extract", response_model=ExtractedTextResponse)
async def extract(file: UploadFile = File(...)):
    """
    Extract text from PDF with OCR fallback.
    1. Tries text-based extraction using pdfplumber
    2. Falls back to OCR if text is empty
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        file_path = tmp_file.name
    
    try:
        # Try text-based extraction first
        raw_text = extract_text_base(file_path)
        
        # If empty, fall back to OCR
        if not raw_text.strip():
            raw_text = ocr_pdf(file_path)
            return {"raw_text": raw_text, "ocr_used": True}
        
        return {"raw_text": raw_text, "ocr_used": False}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)