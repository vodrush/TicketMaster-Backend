# -*- coding: utf-8 -*-
from script import add_ticket, load_tickets, save_tickets, count_by_status, filter_tickets, sort_tickets, update_ticket
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

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data: dict):
    required_fields = ['title', 'description', 'status', 'priority', 'tags']
    for field in required_fields:
        if field not in ticket_data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    new_ticket = add_ticket(tickets, ticket_data)
    save_tickets(TICKETS_FILE, tickets)
    return new_ticket

@app.patch("/tickets/{ticket_id}")
def modify_ticket(ticket_id: int, changes: dict):
    if not changes:
        raise HTTPException(status_code=400, detail="No changes provided")
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