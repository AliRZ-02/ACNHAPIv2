from datetime import datetime

class Date:
    year: int
    month: int
    date: int
    hour: int
    minute: int
    second: int
    
    def __init__(self, year=None, month=None, date=None, hour=None, minute=None, second=None, *, dateObj: datetime = None) -> None:
        if dateObj:
            self.year = dateObj.year
            self.month = dateObj.month
            self.date = dateObj.day
            self.hour = dateObj.hour
            self.minute = dateObj.minute
            self.second = dateObj.second
        else:
            self.year = year
            self.month = month
            self.date = date
            self.hour = hour
            self.minute = minute
            self.second = second
    
    def as_dict(self):
        """Method to return instance data as dictionary"""
        
        return {
            "year": self.year,
            "month": self.month,
            "date": self.date,
            "hour": self.hour,
            "minute": self.minute,
            "second": self.second
        }