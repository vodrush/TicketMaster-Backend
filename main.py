from script import load_tickets, save_tickets , count_by_status, filter_tickets, sort_tickets

tickets = load_tickets('backend/tickets.json')
sorted_by_date = sort_tickets(tickets, key='createdAt', reverse=False)
print(f"Premier ticket (plus ancien): {sorted_by_date[1]['createdAt']}")
