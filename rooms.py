from abc import ABC,abstractmethod
class Room(ABC):
    
    def __init__(self,roomno,roomtype,floornumber):
        self.roomno=roomno
        self.roomtype=roomtype
        self.floornumber=floornumber
    @abstractmethod
    def base_tariffcal(self):
        pass
    @abstractmethod
    def max_guests(self):
        pass
    @abstractmethod
    def extraguestcharges(self,numberofguests):
        pass
    @abstractmethod
    def breakfast_charge(self,numberofguests,include_breakfast=False):
        pass

    def __str__(self):
        return f"roomNO:{self.roomno},roomtype:{self.roomtype},floornumber:{self.floornumber},tariff:{self.base_tariffcal()}"

        

class StandardRoom(Room):
    def __init__(self,roomnumber,roomtype,floornumber):
        super().__init__(roomnumber,roomtype,floornumber)
        self.baseamount=2500
        self.maxguests=2
    def base_tariffcal(self):
        return self.baseamount
    def extraguestcharges(self,numberofguests):
        return 0
    def breakfast_charge(self,numberofguests,include_breakfast=False):
        if include_breakfast:
            return 350*numberofguests
        else:
            return 0
    def max_guests(self):
        return self.maxguests
class DeluxeRoom(Room):
    def __init__(self,roomnumber,roomtype,floornumber):
        super().__init__(roomnumber,roomtype,floornumber)
        self.baseamount=4000
        self.maxguests=3
    def base_tariffcal(self):
        return self.baseamount
    def extraguestcharges(self,numberofguests):
        if numberofguests>2:
            extraguests=numberofguests-2
            return extraguests*800
        else:
            return 0
    def breakfast_charge(self, numberofguests, include_breakfast=False):
        return 0
    def max_guests(self):
        return self.maxguests
class SuiteRoom(Room):
    def __init__(self,roomnumber,roomtype,floornumber):
        super().__init__(roomnumber,roomtype,floornumber)
        self.baseamount=7500
        self.maxguests=4
    def base_tariffcal(self):
        return self.baseamount
    def extraguestcharges(self,numberofguests):
        if numberofguests>2:
            extraguests=numberofguests-2
            return extraguests*800
        else:
            return 0
    def breakfast_charge(self, numberofguests, include_breakfast=False):
        pass
    def max_guests(self):
        return self.maxguests




        
 





        






    

