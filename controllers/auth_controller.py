from models.db import USERS
from models.user import Customer
from controllers.validation import validate_name, validate_email, validate_phone

class AuthController:
    def login(self, username, password):
        if username in USERS:
            user = USERS[username]
            if user['password'] == password:
                # Check if it's a soft-deleted customer
                if user['role'] == 'customer' and not user.get('is_active', True):
                    return False, "It looks like your account has been deactivated. Please contact support."
                return True, user
        return False, "The username or password you entered is incorrect. Please try again."

    def register_customer(self, name, email, phone, address, password):
        # Validation is now handled interactively field-by-field before reaching here.
        username = email # Use email as username

        # Create customer and store
        new_customer = Customer(username, password, name, email, phone, address)
        USERS[username] = new_customer.to_dict()
        return True, "You've been registered successfully! You can now log in using your email."
