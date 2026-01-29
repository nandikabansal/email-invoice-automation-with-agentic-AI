from langgraph.graph import StateGraph, END
from app.state.invoice_state import InvoiceState
from app.agents.email_classifier_wrapper import classify_email_node
from app.agents.document_handler import process_invoice_attachments

# --------------------------------------------------
# Build graph
# --------------------------------------------------
graph = StateGraph(InvoiceState)

graph.add_node("classify", classify_email_node)
graph.add_node("process_invoice", process_invoice_attachments)

# Entry point
graph.set_entry_point("classify")

# --------------------------------------------------
# Router: decides next node based on classifier output
# --------------------------------------------------
def route_from_classifier(state: dict):
    """
    Reads _next_node set by classify_email_node
    """
    next_node = state.get("_next_node")

    if next_node == "process_invoice":
        return "process_invoice"

    return END


# Conditional routing
graph.add_conditional_edges(
    "classify",
    route_from_classifier,
    {
        "process_invoice": "process_invoice",
        END: END
    }
)

# Final edge
graph.add_edge("process_invoice", END)

# Compile graph
invoice_graph = graph.compile()

