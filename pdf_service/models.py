from pydantic import BaseModel

class ExtractedTextResponse(BaseModel):
    raw_text: str
    ocr_used: bool
