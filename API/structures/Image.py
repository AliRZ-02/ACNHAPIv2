class Image:
    location: str
    description: str
    height: float
    width: float
    color: float

    def __init__(self, location: str, description: str, height: float, width: float, color: float) -> None:
        self.location = location
        self.description = description
        self.height = height
        self.width = width
        self.color = color