def send_email(payload: dict):

    print("========== EMAIL ==========")
    print(f"Ticket: {payload['ticket_id']}")
    print(f"Cliente: {payload['client_id']}")
    print(f"Título: {payload['title']}")
    print("===========================")

