class Train:
    def __init__(self, train_no, name, origin, destination, schedule, total_ac_seats, total_sl_seats):
        self.train_no = train_no
        self.name = name
        self.origin = origin
        self.destination = destination
        self.schedule = schedule  # e.g., [{"station": "A", "arrival": "10:00", "departure": "10:15"}, ...]
        self.total_ac_seats = total_ac_seats
        self.total_sl_seats = total_sl_seats
        self.available_ac_seats = total_ac_seats
        self.available_sl_seats = total_sl_seats

    def to_dict(self):
        return {
            "train_no": self.train_no,
            "name": self.name,
            "origin": self.origin,
            "destination": self.destination,
            "schedule": self.schedule,
            "total_ac_seats": self.total_ac_seats,
            "total_sl_seats": self.total_sl_seats,
            "available_ac_seats": self.available_ac_seats,
            "available_sl_seats": self.available_sl_seats
        }
