class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Customer(User):
    def __init__(self, username, password, name, email, phone, address, is_active=True):
        super().__init__(username, password, "customer")
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_active = is_active

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "is_active": self.is_active
        }
