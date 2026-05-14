class Booking:
    def __init__(self, ticket_id, customer_username, train_no, travel_date, origin, destination, seat_class, no_of_tickets, total_fare, status="Confirmed"):
        self.ticket_id = ticket_id
        self.customer_username = customer_username
        self.train_no = train_no
        self.travel_date = travel_date
        self.origin = origin
        self.destination = destination
        self.seat_class = seat_class
        self.no_of_tickets = no_of_tickets
        self.total_fare = total_fare
        self.status = status

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "customer_username": self.customer_username,
            "train_no": self.train_no,
            "travel_date": self.travel_date,
            "origin": self.origin,
            "destination": self.destination,
            "seat_class": self.seat_class,
            "no_of_tickets": self.no_of_tickets,
            "total_fare": self.total_fare,
            "status": self.status
        }
