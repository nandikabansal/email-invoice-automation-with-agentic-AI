# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.services.text_extractor import extract_text_from_pdf

# router = APIRouter()


# @router.post("/extract")
# async def extract_text(file: UploadFile = File(...)):
#     """
#     Extract text from PDF.
#     Uses OCR if text layer is missing.
#     """
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files supported")

#     raw_text = extract_text_from_pdf(file)

#     return {
#         "raw_text": raw_text
#     }


from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter()

PDF_SERVICE_URL = "http://127.0.0.1:8001/extract"


@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from PDF by calling the PDF microservice.
    Uses OCR if text layer is missing.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    try:
        # Forward the file to the PDF microservice
        files = {
            "file": (file.filename, file.file, "application/pdf")
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(PDF_SERVICE_URL, files=files, timeout=120.0)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        return response.json()
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"PDF service unavailable: {str(e)}")