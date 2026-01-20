import json
import datetime

def load_tickets(filepath):
    with open(filepath, 'r') as file:
        tickets = json.load(file)
    return tickets

def save_tickets(filepath, tickets):
    with open(filepath, 'w') as file:
        json.dump(tickets, file, indent=2)
    return tickets

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
    return sorted(tickets, key=lambda x: x[key], reverse=reverse)

def add_ticket(tickets, ticket_data):
    max_id = max(ticket['id'] for ticket in tickets) if tickets else 0
    new_ticket = {
        'id': max_id + 1,
        'createdAt': datetime.datetime.utcnow().isoformat() + 'Z',
        'updatedAt': datetime.datetime.utcnow().isoformat() + 'Z',  # Exemple de date/heure actuelle
        **ticket_data
    }         
    tickets.append(new_ticket)
    return new_ticket
def update_ticket(tickets, ticket_id, changes):
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket.update(changes)
            ticket['updatedAt'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'
            return ticket  