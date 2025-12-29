from typing import TypedDict, Optional, List


class InvoiceState(TypedDict):
    email_id: str
    email_subject: str
    email_body: str

    attachments: List[str]

    is_invoice: Optional[bool]
    classification_confidence: Optional[float]

    raw_text: Optional[str]
    extracted_data: Optional[dict]

    validation_status: Optional[str]
