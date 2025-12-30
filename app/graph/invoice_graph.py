from langgraph.graph import StateGraph, END
from app.state.invoice_state import InvoiceState
from app.agents.email_classifier import classify_email  # NEW AGENT

graph = StateGraph(InvoiceState)

graph.add_node("classify", classify_email)
graph.set_entry_point("classify")
graph.add_edge("classify", END)

invoice_graph = graph.compile()

