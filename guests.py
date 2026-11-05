class guest():
    def __init__(self,guestname,mobilenumber,email):
        self.guestname=guestname
        self.__mobilenumber=mobilenumber
        self.email=email
        # if guestname.strip()=="":
        #     print(f"guestname is empty")
        # if mobilenumber=="":
        #     print(f"mobilenumber is empty")
        # if len(str(mobilenumber))!=10:
        #     print(f"mobilenumber is not 10 digit number ")
        # if str(mobilenumber)[0] not in "6789":
        #     print(f"mobilenumber not starting with 6789")
        # try:
        #     mobilenumber=int(mobilenumber)
        # except ValueError:
        #     print("mobilenumber is not valid")
        # if email =="":
        #     print(f"email is empty")
        # if not email.endswith("@gmail.com"):
        #     print("Invalid email")
    def get_mobilenumber(self):
        return self.__mobilenumber
    def __str__(self):
        return f"guestname:{self.guestname},guestmobilenumber:{self.__mobilenumber},email:{self.email}"

