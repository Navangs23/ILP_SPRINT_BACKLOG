from views.main_view import main_menu, get_login_details, get_registration_details, display_message, CancelOperationException
from controllers.auth_controller import AuthController
from controllers.admin_controller import AdminController
from controllers.customer_controller import CustomerController

def main():
    auth_controller = AuthController()
    admin_controller = AdminController()
    customer_controller = CustomerController()

    while True:
        choice = main_menu()
        
        try:
            if choice == '1':
                username, password = get_login_details()
                success, result = auth_controller.login(username, password)
                if success:
                    user = result
                    display_message(f"Welcome, {user.get('name', user['username'])}!")
                    if user['role'] == 'admin':
                        admin_controller.handle_admin_flow(user)
                    elif user['role'] == 'customer':
                        customer_controller.handle_customer_flow(user)
                else:
                    display_message(result, False)
                    
            elif choice == '2':
                # Pass USERS for validation
                from models.db import USERS
                name, email, phone, address, password = get_registration_details(USERS)
                success, message = auth_controller.register_customer(name, email, phone, address, password)
                display_message(message, success)
                
            elif choice == '3':
                print("Good Bye User!!. Terminating the Program")
                break
                
            else:
                print("You have selected an inappropriate option. Kindly select an appropriate option.")
        except CancelOperationException:
            print("\n[INFO] Operation cancelled by user. Returning to Main Menu.")

if __name__ == "__main__":
    main()
