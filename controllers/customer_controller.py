from models.db import USERS, TRAINS, BOOKINGS
import models.db as db
from models.booking import Booking
from views.customer_view import (
    customer_menu, get_profile_update_details, confirm_soft_delete,
    get_search_criteria, display_trains, get_booking_details,
    confirm_booking, get_cancellation_details, display_booking_history
)
from views.main_view import display_message
from controllers.validation import validate_name, validate_phone, validate_date

class CustomerController:
    def handle_customer_flow(self, user):
        self.current_user = user
        while True:
            choice = customer_menu()
            if choice == '1':
                self.update_profile()
            elif choice == '2':
                if self.soft_delete():
                    break # Logout on deactivate
            elif choice == '3':
                self.search_trains()
            elif choice == '4':
                self.book_ticket()
            elif choice == '5':
                self.cancel_ticket()
            elif choice == '6':
                self.view_history()
            elif choice == '7':
                print("Good Bye User!!. Logging out.")
                break
            else:
                print("You have selected an inappropriate option. Kindly select an appropriate option.")

    def update_profile(self):
        name, phone, address = get_profile_update_details(self.current_user)
        
        if name and not validate_name(name):
            display_message("Update Failed: Name should not contain numeric or special characters.", False)
            return
        if phone and not validate_phone(phone):
            display_message("Update Failed: Phone must be exact 10 digits.", False)
            return

        if name: self.current_user['name'] = name
        if phone: self.current_user['phone'] = phone
        if address: self.current_user['address'] = address
        
        username = self.current_user['username']
        USERS[username] = self.current_user
        display_message("Profile Updated Successfully!")

    def soft_delete(self):
        if confirm_soft_delete():
            username = self.current_user['username']
            USERS[username]['is_active'] = False
            display_message("Your account has been deactivated successfully. Logging out...")
            return True
        return False

    def search_trains(self):
        origin, destination, date_str = get_search_criteria()
            
        available_trains = []
        for t_no, train in TRAINS.items():
            schedule = train.get('schedule', {})
            # Check if origin and destination exist
            if origin in schedule and destination in schedule:
                available_trains.append(train)
                
        display_trains(available_trains)

    def book_ticket(self):
        train_no, travel_date, origin, destination, seat_class, no_of_tickets = get_booking_details(TRAINS)
            
        train = TRAINS[train_no]

        # Check seats
        if seat_class == 'AC':
            base_fare = 1500
        elif seat_class == 'SL':
            base_fare = 500
        else:
            display_message("Invalid class selected. Please use AC or SL.", False)
            return

        # Simple fare calculation
        total_fare = base_fare * no_of_tickets

        if confirm_booking(total_fare):
            # Update seats
            if seat_class == 'AC':
                TRAINS[train_no]['available_ac_seats'] -= no_of_tickets
            else:
                TRAINS[train_no]['available_sl_seats'] -= no_of_tickets

            # Create booking
            ticket_id = f"TKT{db.NEXT_TICKET_ID}"
            db.NEXT_TICKET_ID += 1
            
            new_booking = Booking(ticket_id, self.current_user['username'], train_no, travel_date, origin, destination, seat_class, no_of_tickets, total_fare)
            BOOKINGS[ticket_id] = new_booking.to_dict()
            
            display_message(f"Your booking is confirmed! Your Ticket ID is {ticket_id}. Have a great trip!")
        else:
            display_message("Okay, we've cancelled your booking process.")

    def cancel_ticket(self):
        ticket_id = get_cancellation_details(BOOKINGS, self.current_user['username'], self.current_user['password'])
        booking = BOOKINGS[ticket_id]
            
        # Release seats
        train_no = booking['train_no']
        seat_class = booking['seat_class']
        no_of_tickets = booking['no_of_tickets']
        
        if train_no in TRAINS:
            if seat_class == 'AC':
                TRAINS[train_no]['available_ac_seats'] += no_of_tickets
            else:
                TRAINS[train_no]['available_sl_seats'] += no_of_tickets

        # Update status
        BOOKINGS[ticket_id]['status'] = 'Cancelled (User Request)'
        display_message("Your ticket has been cancelled successfully. Your refund has been initiated.")

    def view_history(self):
        user_bookings = [b for b in BOOKINGS.values() if b['customer_username'] == self.current_user['username']]
        display_booking_history(user_bookings)
