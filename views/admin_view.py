from views.main_view import print_header, display_message, get_validated_input
from controllers.validation import validate_time_format, validate_name , validate_train_number
from controllers.validation import validate_datetime_format, is_after
from datetime import datetime

def admin_menu():
    print_header("Admin Dashboard")
    print("1) Admin Train Registration")
    print("2) Train Details Update by Admin")
    print("3) Delete Train by Admin")
    print("4) Exit")
    return input("Select an option (1-4): ")

def get_train_details(TRAINS):
    print_header("Train Registration")
    print("Type 'cancel' at any time to return to the menu.")
    
    def validate_unique(tno):
        from controllers.validation import validate_train_number_unique
        if not validate_train_number_unique(tno, TRAINS):
            print("\n[ERROR] A train with this number already exists. Please use a unique train number.")
            return False
        return True

    train_no = get_validated_input("Train Number (e.g. 12345): ", validate_train_number, "Invalid Train Number.", required=True)
    name = get_validated_input("Train Name (e.g. Express Train): ", validate_name, "Name must contain only alphabets and spaces.", required=True)
    origin = get_validated_input("Origin Station (e.g. Dadar): ", required=True)
    destination = get_validated_input("Destination Station (e.g. Surat): ", required=True)
    
    print("\n--- Schedule Details ---")
    schedule = {}
    base_datetime = None
    last_departure = None
    while True:
        station = get_validated_input("Enter Station Name (or type 'done' to finish): ", validate_name, "Station name must contain only alphabets and spaces.", required=True)
        if station.lower() == 'done':
            if len(schedule) < 2:
                print("\n[ERROR] At least two stations (origin and destination) are required.")
                continue
            break
                
        
        arrival_str = get_validated_input(
                f"Arrival at {station} (DD-MM-YYYY HH:MM): ",
                validate_datetime_format,
                "Invalid format.",
                required=True
            )

        arrival_dt = datetime.strptime(arrival_str, "%d-%m-%Y %H:%M")   
        if base_datetime is None:
                base_datetime = arrival_dt

        day_offset_arr = (arrival_dt.date() - base_datetime.date()).days
        arrival_time = arrival_dt.strftime("%H:%M")

        
        
        if last_departure is not None:
            prev_dt = datetime.strptime(last_departure, "%d-%m-%Y %H:%M")
            if arrival_dt <= prev_dt:
                print("\n[ERROR] Arrival must be after previous departure.")
                continue

        departure_str = get_validated_input(
                f"Departure from {station} (DD-MM-YYYY HH:MM): ",
                validate_datetime_format,
                "Invalid format.",
                required=True
            )

        
        departure_dt = datetime.strptime(departure_str, "%d-%m-%Y %H:%M")
        if departure_dt <= arrival_dt:
            print("\n[ERROR] Departure must be after arrival.")
            continue

        
        day_offset_dep = (departure_dt.date() - base_datetime.date()).days
        departure_time = departure_dt.strftime("%H:%M")


        
        schedule[station] = {
                'arrival_time': arrival_time,
                'arrival_day': day_offset_arr,
                'departure_time': departure_time,
                'departure_day': day_offset_dep
            }

        last_departure = departure_str
        
    def validate_seats(n): return n.isdigit() and int(n) >= 0
    total_ac_seats = int(get_validated_input("Total AC Seats (e.g. 50): ", validate_seats, "Must be a positive integer.", required=True))
    total_sl_seats = int(get_validated_input("Total Sleeper Seats (e.g. 200): ", validate_seats, "Must be a positive integer.", required=True))

    return train_no, name, origin, destination, schedule, total_ac_seats, total_sl_seats

def get_train_number(action, TRAINS):
    print_header(f"{action.capitalize()} Train")
    print("Type 'cancel' at any time to return to the menu.")
    
    def validate_exists(tno):
        if tno not in TRAINS:
            print("\n[ERROR] We couldn't find a train with that number.")
            return False
        return True

    return get_validated_input("Enter Train Number (e.g. 12345): ", validate_exists, "Train not found.", required=True)

def get_train_update_details(train):
    print_header(f"Update Train: {train['name']} ({train['train_no']})")
    print("Leave field blank to keep current value.")
    
    name = get_validated_input(f"Train Name [{train['name']}]: ", required=False)
    name = name or train['name']
    
    origin = get_validated_input(f"Origin Station [{train['origin']}]: ", required=False)
    origin = origin or train['origin']
    
    destination = get_validated_input(f"Destination Station [{train['destination']}]: ", required=False)
    destination = destination or train['destination']
    
    print("\n--- Update Schedule (Current Schedule printed below) ---")
    for st, times in train['schedule'].items():
        print(f"Station: {st}, Arrival: {times['arrival']}, Departure: {times['departure']}")
    
    update_schedule_choice = get_validated_input("Do you want to update the schedule? (yes/no): ", lambda x: x.lower() in ['yes', 'no'], "Please answer yes or no.", required=True)
    schedule = train['schedule']
    if update_schedule_choice.lower() == 'yes':
        schedule = {}
        while True:
            station = get_validated_input("Enter Station Name (or type 'done' to finish): ", required=True)
            if station.lower() == 'done':
                if len(schedule) < 2:
                    print("\n[ERROR] At least two stations required.")
                    continue
                break
            arrival = get_validated_input(f"Arrival time at {station} (e.g. 14:30): ", validate_time_format, "Invalid time format. Use HH:MM.", required=True)
            departure = get_validated_input(f"Departure time at {station} (e.g. 14:45): ", validate_time_format, "Invalid time format. Use HH:MM.", required=True)
            schedule[station] = {'arrival': arrival, 'departure': departure}
            
    return name, origin, destination, schedule
