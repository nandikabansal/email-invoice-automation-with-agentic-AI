import tempfile
import shutil
import os
from app.services.ocr import ocr_pdf


def extract_text_from_pdf(upload_file):
    """
    1. Try text-based extraction
    2. If empty → fallback to OCR
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(upload_file.file, tmp)
        pdf_path = tmp.name

    try:
        import pdfplumber

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            return text

        # Fallback to OCR
        return ocr_pdf(pdf_path)

    finally:
        os.remove(pdf_path)
