from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
import shutil
import os

from app.graph.invoice_graph import invoice_graph
from app.state.invoice_state import InvoiceState

router = APIRouter(prefix="/manual", tags=["Manual Input"])


@router.post("/process")
async def process_email(
    subject: str = Form(...),
    body: str = Form(...),
    pdf: UploadFile = File(...)
):
    """
    Manually submit an email + PDF invoice for processing
    """

    # --- Save PDF to a temp file ---
    try:
        print("Subject", subject)
        print("pdf data received", pdf)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(pdf.file, tmp)
            pdf_path = tmp.name
    finally:
        pdf.file.close()

    # --- Initial LangGraph state ---
    state: InvoiceState = {
        "email_subject": subject,
        "email_body": body,
        "attachments": [pdf_path],   # <-- FILE PATHS ONLY
        "is_invoice": None,
        "classification_confidence": None,
        "raw_text": None,
        "extracted_data": None,
        "validation_status": None,
    }

    try:
        result = invoice_graph.invoke(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optional cleanup
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
