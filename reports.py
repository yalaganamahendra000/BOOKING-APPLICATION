from datetime import datetime,timedelta
from room_validator import roomobjects
import databaseaccess

def occupancy_report():

    start_date = input("Enter start date (DD-MM-YYYY): ")
    end_date = input("Enter end date (DD-MM-YYYY): ")

    try:
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

    except ValueError:
        print("Enter valid dates")
        return

    if end_date <= start_date:
        print("End date must be after start date")
        return

    total_rooms = len(roomobjects)

    if total_rooms == 0:
        print("No rooms available in the data")
        return

    cursor = databaseaccess.cursor

    current_date = start_date

    total_occupancy = 0
    number_of_nights = 0

    print("---ocupancy report:-----")

    while current_date < end_date:

        date_db = current_date.strftime("%Y-%m-%d")

        cursor.execute(""" SELECT COUNT(DISTINCT roomno) FROM bookings WHERE UPPER(bookingstatus) IN ('CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT') AND checkin <= ? AND checkout > ? """, (date_db, date_db))

        occupied_rooms = cursor.fetchone()[0]

        occupancy_percentage = (occupied_rooms / total_rooms) * 100

        print("\ndate--:", current_date)
        print("Occupied Rooms:", occupied_rooms)
        print("total rooms:", total_rooms)
        print("occupancy percentage:", round(occupancy_percentage, 2), "%")

        total_occupancy = total_occupancy + occupancy_percentage
        number_of_nights = number_of_nights + 1

        current_date = current_date + timedelta(days=1)

    average_occupancy = total_occupancy / number_of_nights

    print("sumary will be:")
    print("average occupancy:", round(average_occupancy, 2), "%")

def revenue_report():
    cursor = databaseaccess.cursor

    room_types = ["standard", "deluxe", "suite"]

    print("\n---revenue report---")

    for roomtype in room_types:

        cursor.execute(""" SELECT COUNT(*), SUM(roomcharges), SUM(gstamount)FROM bookings WHERE LOWER(roomtype) = ? AND bookingstatus = 'CHECKED_OUT' """, (roomtype,))

        result = cursor.fetchone()

        completed_stays = result[0]
        room_revenue = result[1]
        gst_collected = result[2]

        if room_revenue is None:
            room_revenue = 0

        if gst_collected is None:
            gst_collected = 0

        cursor.execute(""" SELECT SUM(totalprice - refundamount) FROM bookings WHERE LOWER(roomtype) = ? AND bookingstatus = 'CANCELLED' """, (roomtype,))

        cancellation_amount = cursor.fetchone()[0]

        if cancellation_amount is None:
            cancellation_amount = 0

        print("rooom type:", roomtype)
        print("completed stays for this roomstype:", completed_stays)
        print("room revenue generated for this room :", room_revenue)
        print("GST collected on this room :", gst_collected)
        print("amount Kept from cancellations:", cancellation_amount)
def export_bookings_to_csv():

    cursor = databaseaccess.cursor

    cursor.execute("SELECT * FROM bookings")

    bookings = cursor.fetchall()

    with open("bookings_export.csv", "w") as file:

        file.write("Booking id,Guest name,Mobile number,room number,room type,Check in,Check out,Number Of guests,booking status,total price,room charges,extra Guest Charges,Breakfast Charges,Long Stay Discount,Loyalty Discount,GST Amount,Breakfast Included,Refund Amount\n")

        for booking in bookings:

            row = []

            for value in booking:
                row.append(str(value))

            file.write(",".join(row) + "\n")

    print("\nBookings exported successfully!")
