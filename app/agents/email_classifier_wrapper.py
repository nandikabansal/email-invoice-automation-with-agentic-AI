from app.agents.email_classifier import classify_email

def classify_email_node(state):
    state = classify_email(state) 
    # Decide next node dynamically
    if state["is_invoice"] == True:
        state["_next_node"] = "process_invoice"
    else:
        state["_next_node"] = "END"
    return state