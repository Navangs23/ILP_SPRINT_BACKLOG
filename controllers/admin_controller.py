from models.db import TRAINS, BOOKINGS
from models.train import Train
from views.admin_view import admin_menu, get_train_details, get_train_number, get_train_update_details
from views.main_view import display_message
from controllers.validation import validate_train_number_unique

class AdminController:
    def handle_admin_flow(self, user):
        while True:
            choice = admin_menu()
            if choice == '1':
                self.register_train()
            elif choice == '2':
                self.update_train()
            elif choice == '3':
                self.delete_train()
            elif choice == '4':
                print("Good Bye Admin!!. Logging out.")
                break
            else:
                print("You have selected an inappropriate option. Kindly select an appropriate option.")

    def register_train(self):
        train_no, name, origin, destination, schedule, total_ac, total_sl = get_train_details(TRAINS)
        
        new_train = Train(train_no, name, origin, destination, schedule, total_ac, total_sl)
        TRAINS[train_no] = new_train.to_dict()
        display_message("Train registered successfully!")

    def update_train(self):
        train_no = get_train_number("update", TRAINS)
        train = TRAINS[train_no]
        name, origin, destination, schedule = get_train_update_details(train)
        
        if len(schedule) < 2:
            display_message("A schedule must contain at least 2 stations.", False)
            return

        TRAINS[train_no]['name'] = name
        TRAINS[train_no]['origin'] = origin
        TRAINS[train_no]['destination'] = destination
        TRAINS[train_no]['schedule'] = schedule
        
        display_message("Train details updated successfully!")

    def delete_train(self):
        train_no = get_train_number("delete", TRAINS)
            
        # Cancel associated bookings
        cancelled_count = 0
        for b_id, booking in BOOKINGS.items():
            if booking['train_no'] == train_no and booking['status'] == 'Confirmed':
                BOOKINGS[b_id]['status'] = 'Cancelled (Train Deleted)'
                cancelled_count += 1
                
        del TRAINS[train_no]
        display_message(f"Train deleted successfully. {cancelled_count} associated active bookings were cancelled.")
