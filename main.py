from script import load_tickets, save_tickets , count_by_status, filter_tickets

tickets = load_tickets('backend/tickets.json')
filtered_tickets = filter_tickets(tickets, status="Open")
print("Filtered tickets with status 'Open':", filtered_tickets)
# Test 2 : filtre par priorité
high_priority = filter_tickets(tickets, priority="High")
print(f"High priority: {len(high_priority)}")

# Test 3 : filtre par tag
bug_tickets = filter_tickets(tickets, tag="bug")
print(f"Bug tickets: {len(bug_tickets)}")

# Test 4 : filtre combiné (status + priority)
open_high = filter_tickets(tickets, status="Open", priority="High")
print(f"Open + High: {len(open_high)}")