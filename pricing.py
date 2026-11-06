from datetime import date,timedelta
import databaseaccess

def calculate_price(selected_room,numberofguests,checkin_date,checkout_date,breakfast_included):
    room_charges=0
    breakfast_charges=0
    extra_guests_charges=0
    gst_amount = 0
    nightly_breakdown = []
    breakfast_charge=0
    while checkin_date<checkout_date:
        day=checkin_date.strftime("%a")

        room_charge_per_day=selected_room.base_tariffcal()

        if day=="Fri" or day=="Sat":
            room_charge_per_day=selected_room.base_tariffcal()+(selected_room.base_tariffcal()*20/100)
        room_charges=room_charges+room_charge_per_day
        extra_charges=selected_room.extraguestcharges(numberofguests)
        extra_guests_charges=extra_guests_charges+extra_charges
        daily_amount = room_charge_per_day + extra_charges

        if room_charge_per_day <= 7500:
            gst = daily_amount * 12 / 100
        else:
            gst = daily_amount * 18 / 100

        gst_amount = gst_amount + gst

        if selected_room.roomtype == "standard" and breakfast_included:
            breakfast_charge = selected_room.breakfast_charge(numberofguests, True)

            breakfast_charges = breakfast_charges + breakfast_charge
        nightly_breakdown.append((checkin_date.strftime("%Y-%m-%d"),day,room_charge_per_day,extra_charges,breakfast_charge,gst))

        checkin_date = checkin_date + timedelta(days=1)
    nights=(checkout_date-checkin_date).days

    longstaydiscount=0

    if nights>=7:
        longstaydiscount=room_charges*10/100
    return room_charges,extra_guests_charges,breakfast_charges,longstaydiscount,gst_amount, nightly_breakdown
def calculate_loyalty_discount(mobilenumber, room_charges):

    cursor = databaseaccess.cursor

    cursor.execute("""SELECT COUNT(*)FROM bookings WHERE mobilenumber = ? AND bookingstatus = 'checked_out'""", (mobilenumber,))

    completed_stays = cursor.fetchone()[0]

    loyalty_discount = 0

    if completed_stays >= 3:
        loyalty_discount = room_charges * 5 / 100

    return loyalty_discount
def cal_final_amount(room_charges, extra_guests_charges,
                           breakfast_charges, longstaydiscount,
                           loyalty_discount, gst_amount):

    total_discount = longstaydiscount + loyalty_discount

    total_amount = room_charges + extra_guests_charges + breakfast_charges + gst_amount

    final_amount = total_amount - total_discount

    return final_amount




