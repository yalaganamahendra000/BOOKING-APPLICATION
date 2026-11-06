import sqlite3
connection =sqlite3.connect("database.db")
cursor=connection.cursor()
# cursor.execute("""create table if not exists rooms(roomtype varchar(25),baserate int ,maximum_guests int ,breakfast int)""")
# cursor.execute("select count(*) from rooms")
# rooms=cursor.fetchone()[0]
# if not rooms:
#     cursor.executemany("""Insert into rooms values(?,?,?,?)""",[('standard',2500,2,350),('deluxe',4000,3,0),('suite',7500,4,0)])
#     connection.commit()
# cursor.execute("""create table if not exists guests(mobilenumber int primary key ,guestname varchar(25) not null,email varchar(100))""")
# connection.commit()


cursor.execute("""create table if not exists  bookings(bookingid TEXT PRIMARY KEY,guestname TEXT NOT NULL,mobilenumber int,
    roomno int,
    roomtype TEXT,
    checkin DATE,
    checkout DATE,
    numberofguests int,
    bookingstatus TEXT,
    totalprice int
)
""")
# cursor.execute("ALTER TABLE bookings ADD COLUMN roomcharges REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN extraguestcharges REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN breakfastcharges REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN longstaydiscount REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN loyaltydiscount REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN gstamount REAL DEFAULT 0")

# cursor.execute("ALTER TABLE bookings ADD COLUMN breakfastincluded INTEGER DEFAULT 0")

# connection.commit()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS booking_nights (
        bookingid TEXT,
        staydate DATE,
        day TEXT,
        roomcharge REAL,
        extraguestcharge REAL,
        breakfastcharge REAL,
        gstamount REAL,
        FOREIGN KEY (bookingid) REFERENCES bookings(bookingid)
    )
""")

connection.commit()
# cursor.execute("""ALTER TABLE bookings ADD COLUMN refundamount REAL DEFAULT 0""")

# connection.commit()


