from controllers.validation import validate_name, validate_email, validate_phone

def print_header(title):
    print("\n" + "="*50)
    print(f"{title.center(50)}")
    print("="*50)

def main_menu():
    print_header("Train Ticket Booking System")
    print("1. Login")
    print("2. Register as Customer")
    print("3. Exit")
    return input("Select an option (1-3): ")

def get_login_details():
    print_header("Login")
    print("Type 'cancel' at any time to return to the menu.")
    username = get_validated_input("Enter UserName (e.g. Email for Customers): ")
    password = get_validated_input("Enter Password: ")
    return username, password

class CancelOperationException(Exception):
    pass

def get_validated_input(prompt, validation_func=None, error_msg="Invalid input.", required=True):
    if required and not prompt.startswith("*"):
        prompt = f"* {prompt}"
    
    while True:
        value = input(prompt).strip()
        
        if value.lower() == 'cancel':
            raise CancelOperationException()
            
        if not value:
            if required:
                print("\n[ERROR] This field is required and cannot be blank.")
                continue
            else:
                return value
        
        if validation_func and not validation_func(value):
            print(f"\n[ERROR] {error_msg}")
            continue
            
        return value

def get_registration_details(USERS=None):
    print_header("Customer Registration")
    print("Please enter the following details to register (type 'cancel' to exit):")
    
    name = get_validated_input("Name (Alphabets only, e.g. John Doe): ", validate_name, "Name must contain only alphabets and spaces.")
    
    def validate_unique_email(email):
        if not validate_email(email):
            print("\n[ERROR] Invalid email format.")
            return False
        if USERS and email in USERS:
            print("\n[ERROR] An account with this email already exists.")
            return False
        return True

    email = get_validated_input("Email (e.g. user@example.com): ", validate_unique_email, "Please provide a valid, unique email address.")
    phone = get_validated_input("Phone Number (10 digits, e.g. 9876543210): ", validate_phone, "Phone number must contain exactly 10 digits.")
    address = get_validated_input("Address (e.g. 123 Main St, City): ", required=True)
    password = get_validated_input("Choose a Password: ", required=True)
    return name, email, phone, address, password

def display_message(message, success=True):
    if success:
        print(f"\n[SUCCESS] {message}")
    else:
        print(f"\n[ERROR] {message}")
