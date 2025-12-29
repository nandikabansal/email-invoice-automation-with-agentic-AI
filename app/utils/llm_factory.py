from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import GEMINI_API_KEY


def get_gemini_llm(
    model: str = "gemini-1.5-flash",
    temperature: float = 0.0
):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GEMINI_API_KEY,
        temperature=temperature
    )
