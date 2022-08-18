from typing import List, Optional

class AvailabilityData:
    month_northern: Optional[str]
    month_southern: Optional[str]
    time: Optional[str]
    isAllDay: Optional[bool]
    isAllYear: Optional[bool]
    location: Optional[str]
    rarity: Optional[str]
    month_array_northern: Optional[List[int]]
    month_array_southern: Optional[List[int]]
    time_array: Optional[List[int]]

    def __init__(self) -> None:
        self.month_northern = None
        self.month_southern = None
        self.time = None
        self.isAllDay = None
        self.isAllYear = None
        self.location = None
        self.rarity = None
        self.month_array_northern = None
        self.month_array_southern = None
        self.time_array = None
    
    def as_dict(self):
        """Method to return data as a dictionary"""
        
        return {
            'month_northern': self.month_northern,
            'month_southern': self.month_southern,
            'time': self.time,
            'isAllDay': self.isAllDay,
            'isAllYear': self.isAllYear,
            'location': self.location,
            'rarity': self.rarity,
            'month_array_northern': self.month_array_northern,
            'month_array_southern': self.month_array_southern,
            'time_array': self.time_array,
        }