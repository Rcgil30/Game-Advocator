from abc import ABC
from typing import overload

class Attributes():
    #Abstract class to define the attributez of each game
    def __init__(self, id: int, title: str, cover: str, releaseYear: int, genre: str, platform: list[str], developer: str, diff: float) -> None:
        self.id = id
        self.title = title
        self.cover = cover
        self.releaseYear = releaseYear
        self.genre = genre
        self.platform = platform
        self.developer = developer
        self.diff = diff
    
    #Description of the game (Only the title)
    def __repr__(self) -> str:
        return f"Title: {self.title}"

class Games(Attributes):
    #Building the game using Attributes constructor
    def __init__(self, id: int, title: str, cover: str, releaseYear: int, genre: str, platform: list[str], developer: str, diff: float) -> None:
        super().__init__(id, title, cover, releaseYear, genre, platform, developer, diff)
    
    #Verifying the game is in the database
    def inDatabase() -> bool:
        pass



class ClassificationAlgorithm(ABC):
    #Definition of classification Metho
    def similars(self):
        ...

class Selections():
    #Constructor for user inputs
    def __init__(self, genre: list[str], platforms: list[str], developer: str, diff: float) -> None:
        self.Usergenre = genre
        self.Userplatforms = platforms
        self.Userdeveloper = developer
        self.Userdiff = diff

    #Method to get the information from the user's inputs
    def getinfo():
        pass

class GameDatabase():
    #Database with all the games to use for classification
    def __init__(self, list_of_games: list[Games]) -> None:
        #We will acces the database of games with an API and get them here
        self.list_of_games = list_of_games

class Classifier(ClassificationAlgorithm):
    def __init__(self, dtb: GameDatabase, selections: Selections) -> None:
        self.dtb = dtb
        self.selections = selections
        self.result = None

    @overload
    #Implementation of Classification Method
    def similars(self) -> list[Games]:
        pass

class Recommedation:
    #Games shown as result
    def __init__(self, classifier: Classifier) -> None:
        self.results = classifier.result