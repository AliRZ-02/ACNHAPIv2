class Translations:
    USen: str
    EUen: str
    EUde: str
    EUes: str
    USes: str
    EUfr: str
    USfr: str
    EUit: str
    EUnl: str
    CNzh: str
    TWzh: str
    JPja: str
    KRko: str
    EUru: str

    def __init__(self) -> None:
        self.USen: str = None
        self.EUen: str = None
        self.EUde: str = None
        self.EUes: str = None
        self.USes: str = None
        self.EUfr: str = None
        self.USfr: str = None
        self.EUit: str = None
        self.EUnl: str = None
        self.CNzh: str = None
        self.TWzh: str = None
        self.JPja: str = None
        self.KRko: str = None
        self.EUru: str = None
    
    def as_dict(self):
        """Method to return instance data as a dictionary"""
        
        return {
            'USen': self.USen,
            'EUen': self.EUen,
            'EUde': self.EUde,
            'EUes': self.EUes,
            'USes': self.USes,
            'EUfr': self.EUfr,
            'USfr': self.USfr,
            'EUit': self.EUit,
            'EUnl': self.EUnl,
            'CNzh': self.CNzh,
            'TWzh': self.TWzh,
            'JPja': self.JPja,
            'KRko': self.KRko,
            'EUru': self.EUru
        }

class NameData(Translations):
    def __init__(self) -> None:
        super().__init__()

class CatchTranslationData(Translations):
    def __init__(self) -> None:
        super().__init__()