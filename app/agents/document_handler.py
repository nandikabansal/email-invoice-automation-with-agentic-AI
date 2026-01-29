import requests
import os

PDF_SERVICE_URL = "http://127.0.0.1:8001/extract"
#should this be hardcoded?

def process_invoice_attachments(state: dict) -> dict:
    """
    Sends PDF attachments to the PDF extraction microservice
    """

    attachments = state.get("attachments", [])
    if not attachments:
        print("[DocumentHandler] No attachments found")
        return state

    pdf_path = attachments[0]

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print(f"[DocumentHandler] Sending PDF to service: {pdf_path}")

    with open(pdf_path, "rb") as f:
        files = {
            "file": ("invoice.pdf", f, "application/pdf")
        }

        response = requests.post(
            PDF_SERVICE_URL,
            files=files,
            timeout=120
        )

    if response.status_code != 200:
        print("[DocumentHandler] PDF service error:")
        print(response.text)
        response.raise_for_status()

    data = response.json()

    state.update({
        "raw_text": data.get("raw_text")
    })

    print("[DocumentHandler] Text extracted successfully")
    return state
