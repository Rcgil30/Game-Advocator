from Database import result


"""
Class Declaration
"""

class Attributes():
    """Abstract class to define the attributes of each game"""

    def __init__(self, id: int, title: str, cover: str,
                 releaseYear: int, genre: str, platform: list[str],
                 developer: str) -> None:
        self.id = id
        self.title = title
        self.cover = cover
        self.releaseYear = releaseYear
        self.genre = genre
        self.platform = platform
        self.developer = developer
        self.diff: float = 0

    # Description of the game (Only the title)
    def __repr__(self) -> str:
        return f"Title: {self.title}"

class GameDatabase():
    """Class that loads all the games of the database into a list"""

    def __init__(self, listofgames: list) -> None:
        # Holder to separate the platforms, as games usually have more than 1
        gameplatform = []
        self.listofgames = listofgames
        # result hold all the information (dictionaries) from the database
        # for loop to iterate through each game of the database
        for game in result.get('games'):
            # Clearing the gameplatformlistfor every game
            gameplatform.clear()
            # Iterating through the platforms of each game
            for platform in game.get("platform"):
                # Adding the platforms to the gameplatform list, which is used to construct each game
                gameplatform.append(platform.get("name"))
            # Building every game using the database information
            games = Games(game.get("id"), game.get("title"), game.get("portada"), game.get("releaseYear"), game.get("gender").get("name"),
                          gameplatform, game.get("developer"), game.get("shop"), game.get("diff"))
            # Adding the created game to the list of all games, in the format needed 
            self.listofgames.append(games)


class Games(Attributes):
    """Concrete class of games"""
    # Building the game using Attributes constructor

    def __init__(self, id: str, title: str, cover: str,
                 releaseYear: int, genre: str, platform: list[str],
                 developer: str, shop: str, diff: int) -> None:
        super().__init__(id, title, cover, releaseYear, genre, platform, developer)
        self.shop = shop
        self.diff = diff

    # Verifying the game is in the database
    def inDatabase(self, database: GameDatabase) -> bool:
        """Verifies if a game is on the database based on the game's title"""
        for game in database.listofgames:
            if (self.title == game.title):
                return True
            if (game.id == '40'):
                return False


class Selections():
    """Class that holds the inputs from the user, which are loaded using the tkinter Interface objects"""

    def __init__(self, genre: list[str], platforms: list[str], developer: str, diff: int) -> None:
        self.Usergenre = genre
        self.Userplatforms = platforms
        self.Userdeveloper = developer
        self.Userdiff = diff

    def __repr__(self) -> str:
        return f"genres: {self.Usergenre} \nplatforms: {self.Userplatforms} \ndeveloper: {self.Userdeveloper} \ndifficulty: {self.Userdiff}"


class Collection():
    """Class to hold and filter data in the classification algorithm"""

    def __init__(self) -> None:
        self.counts = []
        self.titles = []
        self.rawdata = []


class Classifier():
    """Class to gather all the other classes and implement the classification method"""

    def __init__(self, dtb: GameDatabase, selections: Selections, collection: Collection) -> None:
        self.dtb = dtb
        self.selections = selections
        self.col = collection

    # Implementation of Classification Method
    def similars(self) -> list[Games]:
        """Classification algorithm that returns final recommendations"""
        # The way the algorithm works is that we compare the characteristics of each game in the database
        # With the selections of the user, aggregating them an arbitrary number of times depending on how similar
        # they are to the lists in Collections class instantiation,
        for game in self.dtb.listofgames:
            # We add gender 4 times, because it is the most important parameter for us
            if (game.genre in self.selections.Usergenre):
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)

            # Since platforms are mostly the same, and are too little, we only add them 2 times in the
            # Calculation of the recommendations
            for platform in game.platform:
                if (platform in self.selections.Userplatforms):
                    self.col.rawdata.append(game.title)
                    self.col.rawdata.append(game.title)
            # If the user puts a developer that we have in our database, we want to show them games of that
            # Developer, so it takes a lot of priority
            if (game.developer == self.selections.Userdeveloper):
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)

            # The game gets added 3 times if the difficulty is the same as the user´s selection,
            # 2 times if its 1 up or down, and 1 time  if the difference is 2, else it doesn't get added
            diff = int(game.diff)
            userdiff = self.selections.Userdiff
            if (diff == userdiff):
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
            elif (userdiff + 1 == diff or userdiff - 1 == diff):
                self.col.rawdata.append(game.title)
                self.col.rawdata.append(game.title)
            elif (userdiff + 2 == diff or userdiff - 2 == diff):
                self.col.rawdata.append(game.title)
        # Here we add each game in order with it's title in the titles list and the amount of times it
        # appears in the raw data with the counts list, so the index in titles represent the same index in counts
        for title in self.col.rawdata:
            if title not in self.col.titles:
                self.col.titles.append(title)
                # count method searches the amount of times an object is present on a list
                self.col.counts.append(self.col.rawdata.count(title))

        # We use bubble sort to organize both lists using the counts list as reference, so that the first titles
        # Correspond to the games that appear more in the raw data we got
        for i in range(len(self.col.counts)):
            for j in range(len(self.col.counts) - i - 1):
                if self.col.counts[j] < self.col.counts[j + 1]:
                    tempc = self.col.counts[j]
                    tempt = self.col.titles[j]
                    self.col.counts[j] = self.col.counts[j + 1]
                    self.col.titles[j] = self.col.titles[j + 1]
                    self.col.counts[j + 1] = tempc
                    self.col.titles[j + 1] = tempt
        # The first, second and third game's titles used as recommendation are assigned to attributes of the class
        self.first = self.col.titles[0]
        self.second = self.col.titles[1]
        self.third = self.col.titles[2]

        # Finally, we itterate through all the database and find the games we got as a result, to then return them in a list
        for game in self.dtb.listofgames:
            if game.title == self.first:
                firstgame = game
            if game.title == self.second:
                secondgame = game
            if game.title == self.third:
                thirdgame = game

        return [firstgame, secondgame, thirdgame]

    def getTitles(self) -> list[str]:
        """Returns list of the first 3 recommendations' titles"""
        return [self.first, self.second, self.third]


class Recommedation:
    """Calls classifier methods in construction and holds the information to be presented to the user"""

    def __init__(self, classifier: Classifier) -> None:
        self.results = classifier.similars()
        self.titles = classifier.getTitles()


