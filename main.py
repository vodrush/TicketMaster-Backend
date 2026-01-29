# -*- coding: utf-8 -*-
from Backend.script import add_ticket, load_tickets, save_tickets, count_by_status, filter_tickets, sort_tickets, update_ticket
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


tickets = load_tickets('backend/tickets.json')
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
    filtered_tickets = filter_tickets(tickets, status, priority, tag)
    sorted_tickets = sort_tickets(filtered_tickets, key=sort_by, reverse=descending)
    return sorted_tickets

@app.post("/tickets")
def create_ticket(ticket_data: dict):
    new_ticket = add_ticket(tickets, ticket_data)
    save_tickets('backend/tickets.json', tickets)
    return new_ticket

@app.patch("/tickets/{ticket_id}")
def modify_ticket(ticket_id: int, changes: dict):
    updated_ticket = update_ticket(tickets, ticket_id, changes)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    save_tickets('backend/tickets.json', tickets)
    return updated_ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    global tickets
    tickets = [ticket for ticket in tickets if ticket['id'] != ticket_id]
    if ticket_id not in [ticket['id'] for ticket in tickets]:
        raise HTTPException(status_code=404, detail="Ticket not found")
    save_tickets('backend/tickets.json', tickets)
    return {"detail": "Ticket deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)