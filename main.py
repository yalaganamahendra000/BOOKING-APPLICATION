import room_validator
from bookings import (search_room_availability,create_booking,check_in,check_out,cancel_booking,view_booking_details,view_stay_history)
from reports import (occupancy_report,revenue_report,export_bookings_to_csv)
def main():
    while True:
        print("_________welcome to stayeasyy hotel:________")
        print("1.Search room availability")
        print("2.create booking")
        print("3.check in")
        print("4.check out and generate invoice")
        print("5.cancel booking")
        print("6.view booking details")
        print("7.view Guest stay history")
        print("8.occupancy report")
        print("9.revenue report")
        print("10.export bookings to CSV")
        print("11.exit")
        choice = input("\nenter Your choice: ")
        if choice=="1":
            search_room_availability()
        if choice == "2":
            create_booking()
        elif choice == "3":
            check_in()
        elif choice == "4":
            check_out()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            view_booking_details()
        elif choice == "7":
            view_stay_history()
        elif choice == "8":
            occupancy_report()
        elif choice == "9":
            revenue_report()
        elif choice == "10":
            export_bookings_to_csv()
        elif choice == "11":
            print("exited, thankyou for visting")
            break
        else:
            print("invalidchoice")
main()