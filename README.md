# TicketMaster Backend

API REST pour gérer des tickets. Construit avec **FastAPI** et **Python**.

## Installation

### Prérequis

- Python 3.8+
- pip

### Étapes

```bash
# Installer les dépendances
pip install fastapi uvicorn

# Lancer le serveur
python main.py
```

Le serveur démarre sur `http://localhost:8000`

## Endpoints API

### GET /tickets

Retourne tous les tickets avec filtres optionnels.

**Paramètres (optionnels):**

- `status` : "Open", "In Progress", "Closed"
- `priority` : "Low", "Medium", "High"
- `tag` : nom du tag
- `sort_by` : "id", "createdAt", "updatedAt", "priority", "status"
- `descending` : true/false

**Exemple:**

```bash
curl http://localhost:8000/tickets?status=Open&sort_by=priority
```

### POST /tickets

Crée un nouveau ticket.

**Body (JSON):**

```json
{
  "title": "Nom du ticket",
  "description": "Description",
  "status": "Open",
  "priority": "Medium",
  "tags": ["feature", "bug"]
}
```

**Exemple:**

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title":"Ajouter login","description":"Page de connexion","status":"Open","priority":"High","tags":["feature"]}'
```

### PATCH /tickets/{id}

Modifie un ticket existant.

**Body (JSON):**
N'importe quel champ du ticket.

**Exemple:**

```bash
curl -X PATCH http://localhost:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"Closed"}'
```

### DELETE /tickets/{id}

Supprime un ticket.

**Exemple:**

```bash
curl -X DELETE http://localhost:8000/tickets/1
```

## Structure du projet

```
.
├── main.py          # API FastAPI + routes
├── script.py        # Fonctions utilitaires (load, save, filter, etc.)
├── tickets.json     # Base de données (stockage JSON)
└── README.md        # Ce fichier
```

## Fichiers principaux

### main.py

Contient la configuration FastAPI et les 4 endpoints principaux.

### script.py

Contient les fonctions pour manipuler les tickets :

- `load_tickets(filepath)` : Charge les tickets
- `save_tickets(filepath, tickets)` : Sauvegarde les tickets
- `add_ticket(tickets, data)` : Ajoute un ticket (auto-incrémente l'ID)
- `update_ticket(tickets, id, changes)` : Modifie un ticket
- `filter_tickets(tickets, status, priority, tag)` : Filtre les tickets
- `sort_tickets(tickets, key, reverse)` : Trie les tickets

### tickets.json

Fichier JSON contenant la liste des tickets. Structure d'un ticket :

```json
{
  "id": 1,
  "title": "Titre",
  "description": "Description",
  "status": "Open",
  "priority": "Medium",
  "tags": ["feature"],
  "createdAt": "2026-01-29T10:00:00Z",
  "updatedAt": "2026-01-29T10:00:00Z"
}
```

## Erreurs

- `400` : Champ manquant ou invalide
- `404` : Ticket non trouvé
- `201` : Ticket créé avec succès

## Notes

- Les données sont stockées en mémoire au démarrage et persistées dans `tickets.json`
- Chaque ticket a un `id` auto-incrémenté
- Les timestamps sont au format ISO 8601 avec timezone UTC

## Voir aussi

Pour le frontend : voir le repo [TicketMaster-Frontend](../TicketMaster-Frontend)
