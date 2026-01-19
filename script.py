import json

def load_tickets(filepath):
    with open(filepath, 'r') as file:
        tickets = json.load(file)
    return tickets

def save_tickets(filepath, tickets):
    with open(filepath, 'w') as file:
        json.dump(tickets, file, indent=2)

def count_by_status(tickets):
    status = {}
    for ticket in tickets:
        stat = ticket['status']
        if stat not in status:
            status[stat] = 0
        status[stat] += 1
    return status

def filter_tickets(tickets, status=None, priority=None, tag=None):
    filtered = []
    for ticket in tickets:
        if (status is None or ticket['status'] == status) and \
           (priority is None or ticket['priority'] == priority) and \
           (tag is None or tag in ticket['tags']):
            filtered.append(ticket)
    return filtered

def sort_tickets(tickets, key='createdAt', reverse=False):
    sorted(tickets, key=lambda x: x[key], reverse=reverse)
    key= 'priority' or 'createdAt'
    reverse= False
    # Retourne la liste triée
    pass