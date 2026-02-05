from script import add_ticket, load_tickets, save_tickets, filter_tickets, sort_tickets, update_ticket
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_FILE = os.path.join(BASE_DIR, 'tickets.json')

tickets = load_tickets(TICKETS_FILE)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tickets")
def get_tickets(status: str = None, priority: str = None, tag: str = None, sort_by: str = 'id', descending: bool = False):
    allowed_sort_keys = ['id', 'createdAt', 'updatedAt', 'priority', 'status']
    if sort_by not in allowed_sort_keys:
        raise HTTPException(status_code=400, detail=f"Invalid sort key: {sort_by}")
    filtered_tickets = filter_tickets(tickets, status, priority, tag)
    sorted_tickets = sort_tickets(filtered_tickets, key=sort_by, reverse=descending)
    return sorted_tickets

VALID_STATUSES = ['Open', 'In Progress', 'Closed']
VALID_PRIORITIES = ['Low', 'Medium', 'High']

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data: dict):
    required_fields = ['title', 'description', 'status', 'priority', 'tags']
    for field in required_fields:
        if field not in ticket_data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    if not isinstance(ticket_data['title'], str) or not ticket_data['title'].strip():
        raise HTTPException(status_code=400, detail="title must be a non-empty string")
    if not isinstance(ticket_data['description'], str):
        raise HTTPException(status_code=400, detail="description must be a string")
    if ticket_data['status'] not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {VALID_STATUSES}")
    if ticket_data['priority'] not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail=f"priority must be one of {VALID_PRIORITIES}")
    if not isinstance(ticket_data['tags'], list) or not all(isinstance(t, str) for t in ticket_data['tags']):
        raise HTTPException(status_code=400, detail="tags must be a list of strings")
    new_ticket = add_ticket(tickets, ticket_data)
    save_tickets(TICKETS_FILE, tickets)
    return new_ticket

@app.patch("/tickets/{ticket_id}")
def modify_ticket(ticket_id: int, changes: dict):
    if not changes:
        raise HTTPException(status_code=400, detail="No changes provided")
    if 'title' in changes and (not isinstance(changes['title'], str) or not changes['title'].strip()):
        raise HTTPException(status_code=400, detail="title must be a non-empty string")
    if 'description' in changes and not isinstance(changes['description'], str):
        raise HTTPException(status_code=400, detail="description must be a string")
    if 'status' in changes and changes['status'] not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {VALID_STATUSES}")
    if 'priority' in changes and changes['priority'] not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail=f"priority must be one of {VALID_PRIORITIES}")
    if 'tags' in changes and (not isinstance(changes['tags'], list) or not all(isinstance(t, str) for t in changes['tags'])):
        raise HTTPException(status_code=400, detail="tags must be a list of strings")
    updated_ticket = update_ticket(tickets, ticket_id, changes)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    save_tickets(TICKETS_FILE, tickets)
    return updated_ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    global tickets
    if ticket_id not in [t['id'] for t in tickets]:
        raise HTTPException(status_code=404, detail="Ticket not found")
    tickets = [t for t in tickets if t['id'] != ticket_id]
    save_tickets(TICKETS_FILE, tickets)
    return {"detail": "Ticket deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)