from views.main_view import print_header, get_validated_input
from controllers.validation import validate_name, validate_phone
from datetime import datetime, timedelta


def customer_menu():
    print_header("Customer Dashboard")
    print("1) Customer Details Update")
    print("2) Customer Soft Delete")
    print("3) Display Available Trains")
    print("4) Train Ticket Booking")
    print("5) Ticket Cancellation")
    print("6) View Booking History")
    print("7) Exit")
    return input("Select an option (1-7): ")

def get_profile_update_details(user):
    print_header("Update Profile")
    print("Leave field blank to keep current value.")
    
    name = get_validated_input(f"Name [{user.get('name', '')}]: ", validate_name, "Name must contain only alphabets and spaces.", required=False)
    name = name or user.get('name', '')
    
    phone = get_validated_input(f"Phone Number [{user.get('phone', '')}]: ", validate_phone, "Phone number must contain exactly 10 digits.", required=False)
    phone = phone or user.get('phone', '')
    
    address = get_validated_input(f"Address [{user.get('address', '')}]: ", required=False)
    address = address or user.get('address', '')
    
    return name, phone, address

def confirm_soft_delete():
    print_header("Deactivate Account")
    confirm = input("Are you sure you want to deactivate your account? (yes/no): ")
    return confirm.lower() == 'yes'

def get_search_criteria():
    print_header("Search Trains")
    print("Type 'cancel' at any time to return to the menu.")
    origin = get_validated_input("Origin Station (e.g. Dadar): ", required=True)
    destination = get_validated_input("Destination Station (e.g. Surat): ", required=True)
    
    from controllers.validation import validate_date
    def check_date(d):
        valid, msg = validate_date(d)
        if not valid:
            print(f"\n[ERROR] {msg}")
            return False
        return True
        
    date_str = get_validated_input("Travel Date (YYYY-MM-DD): ", check_date, "Invalid date.", required=True)
    return origin, destination, date_str

def display_trains(trains, travel_date):
    print_header("Available Trains")
    if not trains:
        print("No trains available for the given criteria.")
        return
    travel_base = datetime.strptime(travel_date, "%Y-%m-%d")    
    for t in trains:
        origin_data = t['schedule'][t['origin']]
        dest_data = t['schedule'][t['destination']]
        origin_dt = travel_base + timedelta(days=origin_data['departure_day'])
        origin_dt = origin_dt.replace(
                hour=int(origin_data['departure_time'].split(':')[0]),
                minute=int(origin_data['departure_time'].split(':')[1])
            )

        dest_dt = travel_base + timedelta(days=dest_data['arrival_day'])  
        dest_dt = dest_dt.replace(
                        hour=int(dest_data['arrival_time'].split(':')[0]),
                        minute=int(dest_data['arrival_time'].split(':')[1])
                    )
        print(f"Train No: {t['train_no']} | Name: {t['name']}")
        print(f"Origin: {t['origin']} (Dep: {origin_dt.strftime('%d-%m-%Y %H:%M')}) "
                    f"-> Destination: {t['destination']} (Arr: {dest_dt.strftime('%d-%m-%Y %H:%M')})")
        print(f"Available Seats -> AC: {t['available_ac_seats']}, Sleeper: {t['available_sl_seats']}")
        print("-" * 40)




def get_booking_details(TRAINS):
    print_header("Book Ticket")
    print("Type 'cancel' at any time to return to the menu.")
    
    def validate_train(tno):
        if tno not in TRAINS:
            print("\n[ERROR] We couldn't find a train with that number.")
            return False
        return True
    train_no = get_validated_input("Enter Train Number (e.g. 12345): ", validate_train, "Train not found.", required=True)
    
    from controllers.validation import validate_date
    def check_date(d):
        valid, msg = validate_date(d)
        if not valid:
            print(f"\n[ERROR] {msg}")
            return False
        return True
    travel_date = get_validated_input("Travel Date (YYYY-MM-DD): ", check_date, "Invalid date.", required=True)
    
    train = TRAINS[train_no]
    def validate_station(st):
        if st not in train['schedule']:
            print("\n[ERROR] This train doesn't stop at that station.")
            return False
        return True
        
    origin = get_validated_input("Origin Station (e.g. Dadar): ", validate_station, "Invalid station.", required=True)
    destination = get_validated_input("Destination Station (e.g. Surat): ", validate_station, "Invalid station.", required=True)
    
    def validate_class(c): return c.upper() in ['AC', 'SL']
    seat_class = get_validated_input("Preferred Class (AC/SL): ", validate_class, "Class must be AC or SL.", required=True).upper()
    
    def validate_tickets(n): 
        if not (n.isdigit() and 1 <= int(n) <= 6):
            return False
        # Check seats
        tickets = int(n)
        if seat_class == 'AC' and train['available_ac_seats'] < tickets:
            print(f"\n[ERROR] Oh no! Only {train['available_ac_seats']} AC seats are left.")
            return False
        elif seat_class == 'SL' and train['available_sl_seats'] < tickets:
            print(f"\n[ERROR] Oh no! Only {train['available_sl_seats']} Sleeper seats are left.")
            return False
        return True
        
    no_of_tickets_str = get_validated_input("Number of Tickets (Max 6): ", validate_tickets, "Must be a number between 1 and 6, and not exceed available seats.", required=True)
    no_of_tickets = int(no_of_tickets_str)
    
    return train_no, travel_date, origin, destination, seat_class, no_of_tickets

def confirm_booking(fare):
    print(f"\nTotal Fare: ${fare}")
    confirm = input("Do you want to confirm this booking? (yes/no): ")
    return confirm.lower() == 'yes'

def get_cancellation_details(BOOKINGS, current_username, current_password):
    print_header("Cancel Ticket")
    print("Type 'cancel' at any time to return to the menu.")
    
    def validate_ticket(tid):
        if tid not in BOOKINGS:
            print("\n[ERROR] We couldn't find a booking with that Ticket ID.")
            return False
        booking = BOOKINGS[tid]
        if booking['customer_username'] != current_username:
            print("\n[ERROR] This ticket does not belong to your account.")
            return False
        if booking['status'] != 'Confirmed':
            print("\n[ERROR] This ticket has already been cancelled.")
            return False
        return True
        
    ticket_id = get_validated_input("Enter Ticket ID (e.g. TKT1): ", validate_ticket, "Invalid Ticket ID.", required=True)
    
    def validate_password(pwd):
        if pwd != current_password:
            print("\n[ERROR] The password you entered is incorrect.")
            return False
        return True
        
    password = get_validated_input("Enter your password to confirm: ", validate_password, "Incorrect password.", required=True)
    return ticket_id

def display_booking_history(bookings):
    print_header("Booking History")
    if not bookings:
        print("No booking history found.")
        return
    for b in bookings:
        print(f"Ticket ID: {b['ticket_id']} | Date: {b['travel_date']} | Status: {b['status']}")
        print(f"Train No: {b['train_no']} | Class: {b['seat_class']} | Tickets: {b['no_of_tickets']}")
        print(f"Route: {b['origin']} -> {b['destination']}")
        print(f"Total Fare: ${b['total_fare']}")
        print("-" * 40)
