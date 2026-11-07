import databaseaccess
from guests import guest
from datetime import datetime, date
import os
from datetime import timedelta
from room_validator import roomobjects
from pricing import calculate_price, calculate_loyalty_discount, cal_final_amount
from exceptions import invalidstatuschange
class Booking:
    def __init__(self, bookingid, bookingstatus="CONFIRMED"):
        self.bookingid = bookingid
        self.__bookingstatus = bookingstatus
    def get_bookingstatus(self):
        return self.__bookingstatus
    def change_status(self, new_status):
        if self.__bookingstatus == "CONFIRMED":
            if new_status == "CHECKED_IN" or new_status == "CANCELLED":
                self.__bookingstatus = new_status
            else:
                raise invalidstatuschange("Invalid status change")
        elif self.__bookingstatus == "CHECKED_IN":
            if new_status == "CHECKED_OUT":
                self.__bookingstatus = new_status
            else:
                raise invalidstatuschange("Invalid status change")
        else:
            raise invalidstatuschange("Status cannot be changed")
    def __str__(self):
        return f"Booking ID: {self.bookingid}, Status: {self.__bookingstatus}"
def search_room_availability():
    cursor = databaseaccess.cursor
    print("\nsearch room availability")
    roomtype = input("enter room type: ").strip().lower()
    if roomtype not in ["standard", "deluxe", "suite"]:
        print("invalid room type.")
        return
    checkin = input("enter check-in date: ")
    checkout = input("enter check-out date: ")
    try:
        checkin_date = datetime.strptime(checkin, "%d-%m-%Y").date()
        checkout_date = datetime.strptime(checkout, "%d-%m-%Y").date()
    except ValueError:
        print("invalid date format.")
        return
    today = date.today()
    if checkin_date < today:
        print("Check-in date cannot be in the past")
        return
    if (checkin_date - today).days > 180:
        print("Check-in date cannot more than 180 days.")
        return
    nights = (checkout_date - checkin_date).days
    if nights < 1 or nights > 30:
        print("you stay only btwn 1 and 30 nights")
        return
    numberofguests = input("enter number of guests: ")
    try:
        numberofguests = int(numberofguests)
    except ValueError:
        print("invalid number of guests.")
        return
    if numberofguests <= 0:
        print("number of guests must be greater than zero.")
        return
    checkin_db = checkin_date.strftime("%Y-%m-%d")
    checkout_db = checkout_date.strftime("%Y-%m-%d")
    cursor.execute("""SELECT roomno FROM bookings WHERE bookingstatus IN ('CONFIRMED', 'CHECKED_IN') AND checkin < ? AND checkout > ? """, (checkout_db, checkin_db))
    booked_rooms = cursor.fetchall()
    unavailable_rooms = []
    for room in booked_rooms:
        unavailable_rooms.append(room[0])
    print("\navailable rooms:")
    available_count = 0
    for room in roomobjects:
        if room.roomtype.lower() == roomtype:
            if room.roomno not in unavailable_rooms:
                if numberofguests <= room.max_guests():
                    available_count += 1
                    print("\nroom number:", room.roomno)
                    print("room type:", room.roomtype)
                    print("floor:", room.floornumber)
                    print("price per night: Rs.", room.base_tariffcal())
    if available_count == 0:
        print("\nNo rooms available for the selected room type and guests number you entered")
    else:
        print("\nTotal Available Rooms:", available_count)
def create_booking():
    while True:
        guestname=input("Enter Guest Name:")
        if guestname=="":
            print("guest cant be empty ")
            continue
        break
    while True:
        try:
            mobilenumber=int(input("enter mobile number:"))        
        except ValueError:
            print("enter valid mobilenumber ")
            continue
        if mobilenumber=="":
            print("empty mobilenumber is not accepted")
            continue
        if len(str(mobilenumber))!=10:
            print("mobilenumber is not 10 digits.")
            continue
        if str(mobilenumber)[0] not  in "6789":
            print("mobilenumber should starts with 6,7,8,9")
            continue
        break
    while True:
        email=input("enter your email:")
        if email=="":
            print("email cannot be empty")
            continue
        if not email.endswith("@gmail.com"):
            print("enter valid email")
            continue
        break
    print("guest validated successfully!")
    Guest=guest(guestname,mobilenumber,email)
    cursor=databaseaccess.cursor
    connection=databaseaccess.connection
    cursor.execute("""select guestname from guests where mobilenumber=?""",(Guest.get_mobilenumber(),))
    result=cursor.fetchone()
    if result is None:
        cursor.execute("""Insert into guests values(?,?,?)""",(Guest.get_mobilenumber(),Guest.guestname,Guest.email,))
        connection.commit()
        print("guests entered succesfully.")
    else:
        print("guests already exists.")
    while True:
        checkin=input("enter your check in date(dd-mm-yyyy)")
        try:
            checkin_date=datetime.strptime(checkin,"%d-%m-%Y")
            today=date.today()
            if checkin_date<today:
                print("checkin cannot be in past.")
                continue
            elif (checkin_date - today).days>180:
                print("cannot checkin 180 days ahead")
            else:
                break
        except ValueError:
            print("check and enter valid date ")
            continue
    while True:
        checkout=input("enter your checkout date(%d-%m-%Y)")
        try:
            checkout_date=datetime.strptime(checkout,"%d-%m-%Y")
            if checkout_date<=checkin_date:
                print("checkout date must be after checkin date ")
                continue
            elif (checkout_date-checkin_date).days>30:
                print("max only 30 nights is allowed.")
                continue
            else:
                numberofnights=checkout_date - checkin_date
                break
        except ValueError:
            print("enter valid checkout date ")
            continue
    while True:
        roomtype = input("Enter room type").strip().lower()
        if roomtype not in ["standard", "deluxe", "suite"]:
            print("room type is not valid .")
            continue
        else:
            break
    while True:
        try:
            numberofguests=int(input("Enter number of guests:"))
            break
        except ValueError:
            print("enter valid guests data")
    if numberofguests > 2 and roomtype == "standard":
        print("You can try Deluxe or Suite room")
    elif numberofguests > 3 and roomtype == "deluxe":
        print("You can try Suite room")

    elif numberofguests > 4:
        print("No room type can accommodate these guests")

    checkin_db = checkin_date.strftime("%Y-%m-%d")
    checkout_db = checkout_date.strftime("%Y-%m-%d")
    selected_room=None
    max_guests_allowed=0
    available_rooms=[]
    alternative_rooms=[]
    if numberofguests<1:
        print("minimum one guest is required.")
        return
    if numberofguests>4:
        print("no room available to accomdate this number of guests ")
        return
    for room in roomobjects:
        if roomtype==room.roomtype and numberofguests<=room.max_guests():
            cursor.execute("""select roomno 
            from bookings where roomno=? and bookingstatus IN ('confirmed','checked_in') and  checkin<? and checkout>?""",(room.roomno,checkout_db,checkin_db))
            result=cursor.fetchone()
            if result is None:
                available_rooms.append(room)
    if len(available_rooms)>0:
        print("available rooms:")
        for room in available_rooms:
            print(room)
        if selected_room is None:
            selected_room=available_rooms[0]
            for room in available_rooms:
                if selected_room.roomno>room.roomno:
                    selected_room=room
    else:
        print("your requested room is not available")
        for room in roomobjects:
            if room.roomtype!=roomtype and numberofguests<=room.max_guests():
                cursor.execute("""select roomno from bookings where roomno=? and bookingstatus in ('confirmed','checked_in') and checkin<? and checkout>?""",(room.roomno,checkout_db,checkin_db))
                result=cursor.fetchone()
                if result is None :
                    if room.roomtype not in alternative_rooms:
                        alternative_rooms.append(room.roomtype)
    if len(alternative_rooms)>0:
        print("Alternative options are :")
        for room in alternative_rooms:
            print(room)
    else:
        print("No other alternative room types  availablee.")
    if selected_room is None:
        return
    breakfast_included = False
    if selected_room.roomtype == "standard":
        while True:
            breakfast = input("Do you want breakfast? (yes/no): ").strip().lower()

            if breakfast == "yes":
                breakfast_included = True
                break
            elif breakfast == "no":
                breakfast_included = False
                break
            else:
                print("Enter yes or no.")
    room_charges, extra_guests_charges, breakfast_charges, longstaydiscount, gst_amount, nightly_breakdown = calculate_price(
    selected_room,numberofguests,checkin_date,checkout_date,breakfast_included)

    loyalty_discount = calculate_loyalty_discount(mobilenumber,room_charges)

    final_amount = cal_final_amount(
        room_charges,
        extra_guests_charges,
        breakfast_charges,
        longstaydiscount,
        loyalty_discount,
        gst_amount)
    print("\ntotal bill")
    print("Selected Room:", selected_room.roomno)
    print("room type:", selected_room.roomtype)
    print("number of nights:", (checkout_date - checkin_date).days)
    print("room charges:", room_charges)
    print("extra guest charges :", extra_guests_charges)
    print("breakfast charges:", breakfast_charges)
    print("longstaydiscount u got is ", longstaydiscount)
    print("loyalty discount is :", loyalty_discount)
    print("Gst applied:", gst_amount)
    print("-----------------------------")
    print("final amount:", final_amount)
    cursor.execute("""SELECT bookingid FROM bookings ORDER BY bookingid DESC LIMIT 1""")

    result = cursor.fetchone()

    if result is None:
        bookingid = "BK0001"
    else:
        last_bookingid = result[0]
        number = int(last_bookingid[2:])
        number = number + 1
        bookingid = "BK" + str(number).zfill(4)

    print("Booking--id:", bookingid)
    while True:
        payment = input("complete full payment ?:").strip().lower()

        if payment == "yes":
            break

        elif payment == "no":
            print("booking is  cancelled--Payment not Done")
            return

        else:
            print("Enter only yes or no")
    cursor.execute("""insert into bookings
    (bookingid, guestname, mobilenumber, roomno, roomtype,checkin, checkout, numberofguests, bookingstatus, totalprice,roomcharges, extraguestcharges, breakfastcharges,longstaydiscount, loyaltydiscount, gstamount, breakfastincluded)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?)""", (bookingid,guestname,mobilenumber,selected_room.roomno,selected_room.roomtype,checkin_db,checkout_db,numberofguests,"CONFIRMED",final_amount,room_charges,extra_guests_charges,breakfast_charges,longstaydiscount,loyalty_discount,gst_amount,1 if breakfast_included else 0))
    connection.commit()
    for night in nightly_breakdown:
        cursor.execute("""
        INSERT INTO booking_nights
        (bookingid, staydate, day, roomcharge,
         extraguestcharge, breakfastcharge, gstamount)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (bookingid,night[0],night[1],night[2],night[3],night[4],night[5]))
        connection.commit()
    print("Booking has succesfully  created")
    print("booking id:", bookingid)
    print("room number:", selected_room.roomno)
    print("booking status : CONFIRMED")
    print("paid total amount is :", final_amount)
def check_in():
    bookingid = input("Enter Booking ID: ")
    cursor = databaseaccess.cursor
    connection = databaseaccess.connection
    cursor.execute("""SELECT bookingid, checkin, bookingstatus FROM bookings WHERE bookingid = ?""", (bookingid,))
    result = cursor.fetchone()
    if result is None:
        print("Booking not found.")
        return
    bookingid = result[0]
    checkin_date = datetime.strptime(result[1], "%Y-%m-%d").date()
    bookingstatus = result[2]
    booking = Booking(bookingid, bookingstatus)
    if bookingstatus != "CONFIRMED":
        print("Only confirmed bookings can be checked in.")
        return
    today = date.today()
    if today < checkin_date:
        print("Check-in date has not came yet please wait .")
        return
    elif today > checkin_date:
        print("Check-in date has already crossed .")
        return
    try:
        booking.change_status("CHECKED_IN")
        cursor.execute("""UPDATE bookings SET bookingstatus = ? WHERE bookingid = ?""", (booking.get_bookingstatus(), bookingid))
        connection.commit()
        print("Check-in is  successful")
        print(booking)
    except invalidstatuschange as error:
        print(error)
def check_out():

    bookingid = input("enter your  booking id: ")

    cursor = databaseaccess.cursor
    connection = databaseaccess.connection

    cursor.execute("""
        SELECT bookingid, bookingstatus
        FROM bookings
        WHERE bookingid = ?
    """, (bookingid,))

    result = cursor.fetchone()

    if result is None:
        print("Booking is not found.")
        return

    bookingid = result[0]
    bookingstatus = result[1]

    booking = Booking(bookingid, bookingstatus)

    try:
        booking.change_status("CHECKED_OUT")

        cursor.execute("""
            UPDATE bookings
            SET bookingstatus = ?
            WHERE bookingid = ?
        """, (booking.get_bookingstatus(), bookingid))

        connection.commit()
        generate_invoice(bookingid)

        print("Check-out is successful")
        print(booking)

    except invalidstatuschange as error:
        print(error)
def cancel_booking():

    bookingid = input("enter booking id:- ")

    cursor = databaseaccess.cursor
    connection = databaseaccess.connection

    cursor.execute("""
        SELECT bookingid, checkin, bookingstatus, totalprice FROM bookings WHERE bookingid = ? """, (bookingid,))

    result = cursor.fetchone()

    if result is None:
        print("Booking not found.")
        return

    bookingid = result[0]
    checkin_date = datetime.strptime(result[1], "%Y-%m-%d").date()
    bookingstatus = result[2]
    totalprice = result[3]

    booking = Booking(bookingid, bookingstatus)

    if bookingstatus != "CONFIRMED":
        print("Only confirmed bookings can be cancelled.")
        return

    days_before_checkin = (checkin_date - date.today()).days

    if days_before_checkin >= 7:
        refundamount = totalprice

    elif days_before_checkin >= 2:
        refundamount = totalprice * 50 / 100

    else:
        refundamount = 0

    try:
        booking.change_status("CANCELLED")

        cursor.execute("""
            UPDATE bookings
            SET bookingstatus = ?, refundamount = ?
            WHERE bookingid = ?
        """, (
            booking.get_bookingstatus(),
            refundamount,
            bookingid
        ))

        connection.commit()

        print("Booking cancelled successfully.")
        print("Booking ID:", bookingid)
        print("Refund Amount:", refundamount)

    except invalidstatuschange as error:
        print(error)
def view_booking_details():

    bookingid = input("Enter Booking ID: ")

    cursor = databaseaccess.cursor

    cursor.execute("""SELECT bookingid, guestname, mobilenumber, roomno,roomtype, checkin, checkout, numberofguests,bookingstatus, totalprice, roomcharges,extraguestcharges, breakfastcharges,longstaydiscount, loyaltydiscount,
               gstamount, refundamount FROM bookings WHERE bookingid = ?""", (bookingid,))

    result = cursor.fetchone()

    if result is None:
        print("Booking not found.")
        return

    print("----booking details----")

    print("Booking ID:", result[0])
    print("Guest Name:", result[1])
    print("Mobile Number:", result[2])
    print("Room Number:", result[3])
    print("Room Type:", result[4])
    print("Check-in Date:", result[5])
    print("Check-out Date:", result[6])
    print("Number of Guests:", result[7])
    print("Booking Status:", result[8])
    print("room charges:", result[10])
    print("extra guest charges:", result[11])
    print("breakfast charges:", result[12])
    print("long stay discount:", result[13])
    print("loyalty discount:", result[14])
    print("GST:", result[15])
    print("total price:", result[9])
    print("refund amount:", result[16])

    print("................")
def view_stay_history():

    mobilenumber = input("Enter Guest Mobile Number: ")

    cursor = databaseaccess.cursor

    cursor.execute("""
        SELECT bookingid, roomno, roomtype, checkin, checkout, bookingstatus, totalprice FROM bookings WHERE mobilenumber = ? ORDER BY checkin DESC """, (mobilenumber,))

    results = cursor.fetchall()

    if len(results) == 0:
        print("no booking history for this guest")
        return

    print("stay history of guest:----")

    for booking in results:

        print("\nBooking ID:", booking[0])
        print("Room Number:", booking[1])
        print("Room Type:", booking[2])
        print("Check-in:", booking[3])
        print("Check-out:", booking[4])
        print("Booking Status:", booking[5])
        print("Total Amount:", booking[6])

        print("-----------------------------------")

    print("Total Bookings:", len(results))
import os

def generate_invoice(bookingid):

    cursor = databaseaccess.cursor

    cursor.execute("""
        SELECT bookingid, guestname, mobilenumber, roomno, roomtype,checkin, checkout, numberofguests, totalprice,roomcharges, extraguestcharges, breakfastcharges,longstaydiscount, loyaltydiscount, gstamount,breakfastincluded
        FROM bookings WHERE bookingid = ?""", (bookingid,))

    result = cursor.fetchone()

    if result is None:
        print("booking is not found.")
        return

    bookingid = result[0]
    guestname = result[1]
    mobilenumber = result[2]
    roomno = result[3]
    roomtype = result[4]
    checkin = result[5]
    checkout = result[6]
    numberofguests = result[7]
    totalprice = result[8]
    roomcharges = result[9]
    extraguestcharges = result[10]
    breakfastcharges = result[11]
    longstaydiscount = result[12]
    loyaltydiscount = result[13]
    gstamount = result[14]
    breakfastincluded = result[15]

    cursor.execute("""
        SELECT email FROM guests
        WHERE mobilenumber = ?
    """, (mobilenumber,))

    guest_result = cursor.fetchone()

    if guest_result is not None:
        email = guest_result[0]
    else:
        email = "Not available"
    cursor.execute("""
    SELECT staydate, day, roomcharge, extraguestcharge,
           breakfastcharge, gstamount FROM booking_nights WHERE bookingid = ? ORDER BY staydate""", (bookingid,))

    nightly_details = cursor.fetchall()

    os.makedirs("invoices", exist_ok=True)

    filename = "invoices/" + bookingid + ".txt"

    with open(filename, "w", encoding="utf-8") as file:

        file.write("Welcome to stayeasy hotel \n")
        file.write("booking details:\n")
        file.write("-----------------------------\n")
        file.write("booking id: " + bookingid + "\n")
        file.write("guest name: " + guestname + "\n")
        file.write("mobile number: " + str(mobilenumber) + "\n")
        file.write("email: " + email + "\n")
        file.write("room number: " + str(roomno) + "\n")
        file.write("room type: " + roomtype + "\n")
        file.write("number of guests: " + str(numberofguests) + "\n")
        file.write("check-in: " + str(checkin) + "\n")
        file.write("check-out: " + str(checkout) + "\n\n")
        file.write("\nnights wise:\n")
        file.write("--------------------------------\n")

        for night in nightly_details:
            file.write("Date: " + str(night[0]) + "\n")
            file.write("Day: " + str(night[1]) + "\n")
            file.write("Room Charge: Rs." + str(night[2]) + "\n")
            file.write("Extra Guest Charge: Rs." + str(night[3]) + "\n")
            file.write("Breakfast Charge: Rs." + str(night[4]) + "\n")
            file.write("GST: Rs." + str(night[5]) + "\n")

        file.write("--------------------------------\n")

        file.write("total price charges:\n")
        file.write("-----------------------------\n")
        file.write("room charges: Rs." + str(roomcharges) + "\n")
        file.write("extra guest charges: Rs." + str(extraguestcharges) + "\n")
        file.write("breakfast included: " + str(breakfastincluded) + "\n")
        file.write("breakfast charges: Rs." + str(breakfastcharges) + "\n")
        file.write("long stay discount: Rs." + str(longstaydiscount) + "\n")
        file.write("loyalty discount: Rs." + str(loyaltydiscount) + "\n")
        file.write("GST: Rs." + str(gstamount) + "\n")

        file.write("-----------------------------\n")
        file.write("Total paid is: Rs." + str(totalprice) + "\n")
        

    print("Invoice generated successfully!")



                
    


    
