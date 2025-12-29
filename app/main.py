from app.graph.invoice_graph import invoice_graph

if __name__ == "__main__":
    initial_state = {
        "email_id": "test-001",
        "email_subject": "Invoice for March",
        "email_body": "Please find attached invoice",
        "attachments": []
    }

    result = invoice_graph.invoke(initial_state)
    print("\nFinal State:")
    print(result)
