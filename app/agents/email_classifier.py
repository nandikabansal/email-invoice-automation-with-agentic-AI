# from app.utils.llm_factory import get_gemini_llm

# def classify_email(state: dict) -> dict:
#     """
#     LLM-based email classification using Gemini.
#     Returns updated state with is_invoice and confidence.
#     """
#     llm = get_gemini_llm(model="models/gemini-2.5-flash", temperature=0)

#     subject = state.get("email_subject", "")
#     body = state.get("email_body", "")

#     prompt = f"""
# You are an AI that classifies emails. 
# Determine if the following email is an invoice.
# Return ONLY JSON with keys:
# - is_invoice (true/false)
# - confidence (0 to 1)

# Email Subject: {subject}
# Email Body: {body}
# """

#     # Gemini LLM call
#     # response = llm.generate([{"role": "user", "content": prompt}]) #wrong 
#     from langchain_core.messages import HumanMessage

#     response = llm.invoke([
#         HumanMessage(content=prompt)
#     ])


#     # Parse the LLM output safely
#     import json
#     try:
#         data = json.loads(response.generations[0][0].text)
#         is_invoice = data.get("is_invoice", False)
#         confidence = float(data.get("confidence", 0))
#     except Exception:
#         # Fallback in case LLM fails
#         print ("Exception is being handled!!!!!!!!!")
#         is_invoice = False
#         confidence = 0.0

#     # Update state
#     state.update({
#         "is_invoice": is_invoice,
#         "classification_confidence": confidence
#     })
#     return state


from app.utils.llm_factory import get_gemini_llm
from langchain_core.messages import HumanMessage
import json

def classify_email(state: dict) -> dict:
    llm = get_gemini_llm(
        model="models/gemini-2.5-flash",
        temperature=0
    )

    prompt = f"""
You are an AI email classifier.

Decide whether the following email is an INVOICE.

Return ONLY valid JSON like this:
{{
  "is_invoice": true,
  "confidence": 0.95
}}

Email Subject:
{state.get("email_subject", "")}

Email Body:
{state.get("email_body", "")}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        raw = response.content.strip()

        # Gemini sometimes wraps JSON in ```json
        if raw.startswith("```"):
            raw = raw.strip("```").replace("json", "").strip()

        data = json.loads(raw)

        is_invoice = bool(data.get("is_invoice", False))
        confidence = float(data.get("confidence", 0.0))

    except Exception as e:
        print("Exception is being handled!!!!!!!!!")
        print("RAW GEMINI OUTPUT:")
        print(response.content)
        print("ERROR:", e)

        is_invoice = False
        confidence = 0.0

    state.update({
        "is_invoice": is_invoice,
        "classification_confidence": confidence
    })

    print(f"[Classifier] is_invoice={is_invoice}, confidence={confidence}")
    return state
