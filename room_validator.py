import sqlite3
connection=sqlite3.connect("roomsdata.db")
cursor=connection.cursor()
def readcsv(filename,errorfilename):
    cursor.execute("""create table if not exists roomsdata(roomno int not null primary key,roomtype varchar(25) ,floor int)""")
    roomnumbers=[]
    roomlist=[]
    rooms=["standard","deluxe","suite"]
    file=open(filename,"r")
    error=open(errorfilename,"w")
    next(file)
    linenumber=1
    for line in file:
        print("Processing:", line)
        linenumber+=1
        line=line.strip()
        if line=="":
            error.write(f"{linenumber}:line is empty\n")
            continue
        parts=line.split(",")
        if len(parts)!=3:
            error.write(f"{linenumber}:has invalid number of columns\n")
            continue
        roomno=parts[0]
        roomtype=parts[1].strip().lower()
        floor=parts[2]
        if roomno=="":
            error.write(f"{linenumber}:roomnumber is empty\n")
            print("Error detected:", linenumber)
            continue
        try:
            roomno=int(roomno)
        except ValueError:
            error.write(f"{linenumber} roomno is invalid\n")
            continue
        if roomtype=="":
            error.write(f"{linenumber}:roomtype is empty\n")
            continue
        if roomtype.lower() not in rooms:
            error.write(f"{linenumber}:roomtype is not registered room type\n")
            print("Error detected:", linenumber)
            continue
        if floor=="":
            error.write(f"{linenumber}:floor number is empty\n")
            print("Error detected:", linenumber)
            continue
        try:
            floor=int(floor)
        except ValueError:
            error.write(f"{linenumber}:floornumber is invalid")
            continue
        if roomno in roomnumbers:
            error.write(f"{linenumber}:duplicate room number\n")
            print("Error detected:", linenumber)
            continue
        roomnumbers.append(roomno)
        roomlist.append((roomno,roomtype,floor))
        try:
            cursor.execute("""Insert into roomsdata values(?,?,?)""",(roomno,roomtype,floor))
        except sqlite3.IntegrityError:
            print("this room id is already exists in database")
        connection.commit()
    file.close()
    error.close()
    return roomlist
roomlist=readcsv("rooms.csv","NEWerror.log")
from rooms import StandardRoom,DeluxeRoom,SuiteRoom
def create_objects(roomlist):
    #roomlist=readcsv("rooms.csv","errors.log")
    roomobjects=[]
    for room in roomlist:
        roomno=room[0]
        roomtype=room[1]
        floor=room[2]
        if roomtype.lower()=="standard":
            obj=StandardRoom(roomno,roomtype,floor)
        if roomtype.lower()=="deluxe":
            obj=DeluxeRoom(roomno,roomtype,floor)
        if roomtype.lower()=="suite":
            obj=SuiteRoom(roomno,roomtype,floor)
        roomobjects.append(obj)
    return roomobjects
roomobjects=create_objects(roomlist)

