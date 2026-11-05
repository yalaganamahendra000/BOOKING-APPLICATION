import sqlite3
connection =sqlite3.connect("database.db")
cursor=connection.cursor()
# cursor.execute("""create table if not exists rooms(roomtype varchar(25),baserate int ,maximum_guests int ,breakfast int)""")
# cursor.execute("select count(*) from rooms")
# rooms=cursor.fetchone()[0]
# if not rooms:
#     cursor.executemany("""Insert into rooms values(?,?,?,?)""",[('standard',2500,2,350),('deluxe',4000,3,0),('suite',7500,4,0)])
#     connection.commit()
cursor.execute("""create table if not exists guests(mobilenumber int primary key ,guestname varchar(25) not null,email varchar(100))""")
connection.commit()


#cursor.execute("""create table if not exists bookings(bookingid text primary key,guestname varchar(25),mobilenumber int ,roomno int, roomtype varchar(25),checkin date,checkout date,number of guests int ,status text,totalprice int )""")
