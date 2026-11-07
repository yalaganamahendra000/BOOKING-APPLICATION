class guest():
    def __init__(self,guestname,mobilenumber,email):
        self.guestname=guestname
        self.__mobilenumber=mobilenumber
        self.email=email
    def get_mobilenumber(self):
        return self.__mobilenumber
    def __str__(self):
        return f"guestname:{self.guestname},guestmobilenumber:{self.__mobilenumber},email:{self.email}"

