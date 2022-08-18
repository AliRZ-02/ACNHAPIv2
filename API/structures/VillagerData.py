from typing import Any, Dict, Optional, Union
from API.structures.SearchOutput import SearchOutput
from API.structures.NameData import NameData, CatchTranslationData
from API.structures.Date import Date
from API.helpers.request.request import SearchInput
from aiohttp import ClientSession
from re import findall

class VillagerData(SearchOutput):
    id: int
    file_name: str
    name: NameData
    personality: str
    birthday_str: str
    birthday: Date
    species: str
    gender: str
    subtype: str
    hobby: str
    catch_phrase: str
    icon_uri: str
    image_uri: str
    bubble_color: str
    text_color: str
    saying: str
    catch_translations: CatchTranslationData

    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        super().__init__(session, data)
        self.name = NameData()
        self.birthday = Date()
        self.catch_translations = CatchTranslationData()
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return instance data as a dictionary"""

        return {
            'id': self.id,
            'file_name': self.file_name,
            'name': self.name.as_dict(),
            'personality': self.personality,
            'birthday_str': self.birthday_str,
            'birthday': self.birthday.as_dict(),
            'species': self.species,
            'gender': self.gender,
            'subtype': self.subtype,
            'hobby': self.hobby,
            'catch_phrase': self.catch_phrase,
            'icon_uri': self.icon_uri,
            'image_uri': self.image_uri,
            'bubble_color': self.bubble_color,
            'text_color': self.text_color,
            'saying': self.saying,
            'catch_translations': self.catch_translations.as_dict()
        }
    
    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """ASYNC --- Method to initialize instance with API data"""

        input = await super().initialize()
        self.id = input.get('id', None)
        self.file_name = input.get('file-name', None)
        
        self.name.USen = input.get('name').get('name-USen', None)
        self.name.EUen = input.get('name').get('name-EUen', None)
        self.name.EUde = input.get('name').get('name-EUde', None)
        self.name.EUes = input.get('name').get('name-EUes', None)
        self.name.USes = input.get('name').get('name-USes', None)
        self.name.EUfr = input.get('name').get('name-EUfr', None)
        self.name.USfr = input.get('name').get('name-USfr', None)
        self.name.EUit = input.get('name').get('name-EUit', None)
        self.name.EUnl = input.get('name').get('name-EUnl', None)
        self.name.CNzh = input.get('name').get('name-CNzh', None)
        self.name.TWzh = input.get('name').get('name-TWzh', None)
        self.name.JPja = input.get('name').get('name-JPja', None)
        self.name.KRko = input.get('name').get('name-KRko', None)
        self.name.EUru = input.get('name').get('name-EUru', None)

        self.personality = input.get('personality', None)
        self.birthday_str = input.get('birthday-string', None)
        
        dates = findall(r'\d{1,2}', input.get('birthday', '1/1').strip())
        self.birthday = Date(2020, dates[1], dates[0], None, None, None)
        self.species = input.get('species', None)
        self.gender = input.get('gender', None)
        self.subtype = input.get('subtype', None)
        self.hobby = input.get('hobby', None)
        self.catch_phrase = input.get('catch-phrase', None)
        self.icon_uri = input.get('icon_uri', None)
        self.image_uri = input.get('image_uri', None)
        self.bubble_color = input.get('bubble-color', None)
        self.text_color = input.get('text-color', None)
        self.saying = input.get('saying', None)

        self.catch_translations.USen = input.get('catch-translations').get('catch-USen', None)
        self.catch_translations.EUen = input.get('catch-translations').get('catch-EUen', None)
        self.catch_translations.EUde = input.get('catch-translations').get('catch-EUde', None)
        self.catch_translations.EUes = input.get('catch-translations').get('catch-EUes', None)
        self.catch_translations.USes = input.get('catch-translations').get('catch-USes', None)
        self.catch_translations.EUfr = input.get('catch-translations').get('catch-EUfr', None)
        self.catch_translations.USfr = input.get('catch-translations').get('catch-USfr', None)
        self.catch_translations.EUit = input.get('catch-translations').get('catch-EUit', None)
        self.catch_translations.EUnl = input.get('catch-translations').get('catch-EUnl', None)
        self.catch_translations.CNzh = input.get('catch-translations').get('catch-CNzh', None)
        self.catch_translations.TWzh = input.get('catch-translations').get('catch-TWzh', None)
        self.catch_translations.JPja = input.get('catch-translations').get('catch-JPja', None)
        self.catch_translations.KRko = input.get('catch-translations').get('catch-KRko', None)
        self.catch_translations.EUru = input.get('catch-translations').get('catch-EUru', None)
    
    # Accessor Methods
    def get_pronoun(self):
        return "his" if self.gender.lower() == "male" else "her"
    
    def get_personality(self):
        personality = self.personality.lower()

        if personality == "uchi": return "sisterly"
        elif personality == "jock": return "athletic"
        elif personality == "normal": return "sweet"
        else: return personality
    
    def get_species(self):
        return self.species.lower()
    
    def get_catch_phrase(self):
        return self.catch_phrase.upper()
    
    def generate_tweet(self, month: int, hemisphere: int, mode: int) -> Optional[str]:
        """Method to generate instance data as a condensed tweet"""
        
        super().generate_tweet(month, hemisphere, mode)
        return f"{self.get_catch_phrase()}! Happy Birthday to this {self.get_personality()} {self.get_species()}, {self.name.USen}. Remember to visit {self.get_pronoun()} birthday party and to bring a special gift! {super().add_tags()}"
