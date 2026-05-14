# In-memory storage to simulate a database

USERS = {
    # Default Admin User
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
}

TRAINS = {}
BOOKINGS = {}

# Global counter for generating unique Ticket IDs
NEXT_TICKET_ID = 1000
