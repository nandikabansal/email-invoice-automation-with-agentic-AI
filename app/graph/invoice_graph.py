from langgraph.graph import StateGraph, END
from app.state.invoice_state import InvoiceState


def dummy_classifier(state: InvoiceState) -> InvoiceState:
    print("Dummy classifier running...")
    return {
        **state,
        "is_invoice": True,
        "classification_confidence": 1.0
    }


graph = StateGraph(InvoiceState)

graph.add_node("classify", dummy_classifier)
graph.set_entry_point("classify")
graph.add_edge("classify", END)

invoice_graph = graph.compile()
