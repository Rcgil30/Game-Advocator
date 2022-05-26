import tkinter as tk
from tkinter import ttk
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from tkinter.font import Font
import webbrowser

"""
Fetching of Database
"""

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://gamesdt.herokuapp.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
	games {
		id
		title
		portada
		developer
		releaseYear
		gender {
			name
		}
		platform {
			name
		}
		shop
		diff
	}
}
"""
)


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
        result = client.execute(query)
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


"""
Graphic Interface and Functionality
"""

# Instantiating the database list to make the process of the app faster
Database = GameDatabase([])


# Function to show the main menu to the user
def MainMenu():
    # Reset the window by destroying previous widgets
    for ele in app.winfo_children():
        ele.destroy()
    # tkinter's label is used in this case to include the background image, which is defined in the main algorithm
    bglabel = tk.Label(app, image=bg)
    bglabel.pack()
    # This button makes you switch to the next menu
    mainbutton = tk.Button(app, image=mainbImage, command=Menu2, bg="#44089B", bd=1,
                           relief="flat", overrelief="raised")
    mainbutton.place(x=520, y=565)
    # This button takes you back to the credits menu
    creditsbutton = tk.Button(app, image=creditsImage, bd=1,
                              relief="flat", overrelief="raised", bg="#00A89A", command=CreditsMenu)
    creditsbutton.place(x=15, y=20)


def CreditsMenu():
    # Clears the app
    for ele in app.winfo_children():
        ele.destroy()
    canvac = tk.Canvas(app)
    canvac.pack()
    # Label to show the credits background
    bgclabel = tk.Label(canvac, image=bgc)
    bgclabel.pack()
    # Button that takes you back to the main menu
    backcbutton = tk.Button(canvac, image=backImage2, bd=1, relief="flat",
                            overrelief="raised", bg="#00A89A", command=MainMenu)
    backcbutton.place(x=10, y=670)


def Menu2():
    # For loop to clear all the widgets from the root, so that we can start with the next menu
    for ele in app.winfo_children():
        ele.destroy()
    # In this canva we will show all the elements for the next menu
    canva = tk.Canvas(app)
    canva.pack()
    # Label to show the background for the second menu
    bg2label = tk.Label(canva, image=bg2)
    bg2label.pack()
    # Making a button to go back to the main menu
    backButton = tk.Button(canva, image=backImage, height=40, width=40, bd=1,
                           relief="flat", overrelief="raised", bg="#FFCBB4", command=MainMenu)
    backButton.place(x=10, y=670)
    # Making this global variables so that they can be used for the gathering of the selections in the getInfo method
    global swAction, swAdventure, swCoop, swFighting, swFps
    global swHorror, swParty, swPc, swPst, swRpg, swSurvival
    global swStrategy, swSwitch, swXbox, difficulty, developerEntry

    # Switch that determines if a checkbutton is selected
    swAction = tk.BooleanVar()
    # We create a button with every Genre to allow the user to click a bunch of them, so that they
    # can select multiple genres, generating then a list of genres, this will happen in the button to
    # show the results
    ActionButton = ttk.Checkbutton(canva, text="Action", variable=swAction)
    ActionButton.place(x=190, y=250)

    swAdventure = tk.BooleanVar()
    # We build each button with the text of the Genre name and de variable that determines
    # If it is selected or not, which we'll use then to get the elements of the list
    AdventureButton = ttk.Checkbutton(
        canva, text="Adventure", variable=swAdventure)
    # With the place method, we get the buttons in a specific pixel of the window
    AdventureButton.place(x=190, y=290)

    swCoop = tk.BooleanVar()
    CoopButton = ttk.Checkbutton(canva, text="Coop", variable=swCoop)
    CoopButton.place(x=190, y=330)

    swFighting = tk.BooleanVar()
    FightingButton = ttk.Checkbutton(
        canva, text="Fighting", variable=swFighting)
    FightingButton.place(x=190, y=370)

    swFps = tk.BooleanVar()
    FpsButton = ttk.Checkbutton(canva, text="Fps", variable=swFps)
    FpsButton.place(x=190, y=410)

    swHorror = tk.BooleanVar()
    HorrorButton = ttk.Checkbutton(canva, text="Horror", variable=swHorror)
    HorrorButton.place(x=190, y=450)

    swParty = tk.BooleanVar()
    PartyButton = ttk.Checkbutton(canva, text="Party", variable=swParty)
    PartyButton.place(x=190, y=490)

    swRpg = tk.BooleanVar()
    RpgButton = ttk.Checkbutton(canva, text="Rpg", variable=swRpg)
    RpgButton.place(x=190, y=530)

    swStrategy = tk.BooleanVar()
    StrategyButton = ttk.Checkbutton(
        canva, text="Strategy", variable=swStrategy)
    StrategyButton.place(x=190, y=570)

    swSurvival = tk.BooleanVar()
    SurvivalButton = ttk.Checkbutton(
        canva, text="Survival", variable=swSurvival)
    SurvivalButton.place(x=190, y=610)

    # After the Genre checkboxes, we define the Platform checkboxes
    # We use the same methodology as in the Genre ones
    swPc = tk.BooleanVar()
    PcButton = ttk.Checkbutton(
        canva, text="Pc", variable=swPc)
    PcButton.place(x=435, y=250)
    swPst = tk.BooleanVar()
    PstButton = ttk.Checkbutton(
        canva, text="PlayStation", variable=swPst)
    PstButton.place(x=435, y=290)
    swXbox = tk.BooleanVar()
    XboxButton = ttk.Checkbutton(
        canva, text="Xbox", variable=swXbox)
    XboxButton.place(x=435, y=330)
    swSwitch = tk.BooleanVar()
    SwitchButton = ttk.Checkbutton(
        canva, text="Nintendo Switch", variable=swSwitch)
    SwitchButton.place(x=435, y=370)

    # Now we create the scale for the difficulty
    difficulty = tk.IntVar()
    diffScale = tk.Scale(canva, variable=difficulty,
                         from_=1, to=10, orient=tk.HORIZONTAL, bg="#FFCBB4", bd=1,
                         relief="flat", font=40, width=20)
    diffScale.place(x=700, y=260)

    developerEntry = tk.Entry(
        canva, width=15, bg="#FFFFFF", fg="#44089B", font=50)
    developerEntry.place(x=930, y=260)

    # Finally, we define the button to advance to gather the info and show the final results
    ResultsButton = tk.Button(canva, image=recoImage, command=getInfo, bg="#FFCBB4", bd=1,
                              relief="flat", overrelief="raised")
    ResultsButton.place(x=540, y=565)


def getInfo():
    # This lists are used to get the selections from the user
    genreselection = []
    platformselection = []
    # Calling switchassignment to get the genres and plarforms selected by the user
    switchassignment(genreselection=genreselection,
                     platformselection=platformselection)
    diffselection = difficulty.get()
    dev = developerEntry.get()
    global UserSelections
    # Creating the selections object with the information extracted from the database
    UserSelections = Selections(
        genre=genreselection, platforms=platformselection, diff=diffselection, developer=dev.upper())
    menu3()


def switchassignment(genreselection: list[str], platformselection: list[str]):
    """Function to assign the selections by the user to 2 lists, later to be used to build the selections object"""

    # Assignment of switches for the genre category
    if (swAction.get()):
        genreselection.append("ACTION")
    if (swAdventure.get()):
        genreselection.append("ADVENTURE")
    if (swCoop.get()):
        genreselection.append("COOP")
    if (swFighting.get()):
        genreselection.append("FIGHTING")
    if (swFps.get()):
        genreselection.append("FPS")
    if (swHorror.get()):
        genreselection.append("HORROR")
    if (swParty.get()):
        genreselection.append("PARTY")
    if (swRpg.get()):
        genreselection.append("RPG")
    if (swStrategy.get()):
        genreselection.append("STRATEGY")
    if (swSurvival.get()):
        genreselection.append("SURVIVAL")

    # Assignment of switches to the platforms category
    if (swPc.get()):
        platformselection.append("PC")
    if (swPst.get()):
        platformselection.append("PLAYSTATION")
    if (swSwitch.get()):
        platformselection.append("SWITCH")
    if (swXbox.get()):
        platformselection.append("XBOX")


def menu3():
    # Clearing window
    for ele in app.winfo_children():
        ele.destroy()
    canva2 = tk.Canvas(app)
    canva2.pack()
    # Label for the background of the results
    bg3label = tk.Label(canva2, image=bg3)
    bg3label.pack()
    backButton = tk.Button(canva2, image=backImage, height=40, width=40, bd=1,
                           relief="flat", overrelief="raised", bg="#FFCBB4", command=Menu2)
    backButton.place(x=10, y=670)
    # Instantiating collection object that is used internally by the classification
    collection = Collection()
    # Creating the classificator that holds all the information and has the functions that calculate the final recommendations
    classification = Classifier(
        dtb=Database, selections=UserSelections, collection=collection)
    # Making recommendation global to be able to use it in the BuyLink methods
    global recommendation
    # As mentioned before, Recommendation class executes the methods in classifier and holds them in its attributes
    recommendation = Recommedation(classifier=classification)
    # Labels to show the names of the final recommendations
    Title1 = tk.Label(canva2, text=recommendation.titles[0], bg="#44089B", fg="#FFCBB4", font=Font(
        family="Comic Sans MS", size="24"))
    Title1.place(x=200, y=250)
    Title1 = tk.Label(canva2, text=recommendation.titles[1], bg="#44089B", fg="#FFCBB4", font=Font(
        family="Comic Sans MS", size="24"))
    Title1.place(x=200, y=400)
    Title1 = tk.Label(canva2, text=recommendation.titles[2], bg="#44089B", fg="#FFCBB4", font=Font(
        family="Comic Sans MS", size="24"))
    Title1.place(x=200, y=550)
    # Buttons that redirect you to the page to buy each recommendation
    ShopButton1 = tk.Button(canva2, text="Click aquí para comprar", bg="#44089B",
                            fg="#FFCBB4", font=Font(family="Comic Sans MS", size="16"), command=BuyLink1)
    ShopButton1.place(x=800, y=250)
    ShopButton2 = tk.Button(canva2, text="Click aquí para comprar", bg="#44089B",
                            fg="#FFCBB4", font=Font(family="Comic Sans MS", size="16"), command=BuyLink2)
    ShopButton2.place(x=800, y=400)
    ShopButton3 = tk.Button(canva2, text="Click aquí para comprar", bg="#44089B",
                            fg="#FFCBB4", font=Font(family="Comic Sans MS", size="16"), command=BuyLink3)
    ShopButton3.place(x=800, y=550)

# Each game has a link in the database fro the page to buy, which is opened in the following methods,
# which are called as objects in the ShopButtons


def BuyLink1():
    # webbrowser.open() opens a tab in your web browser with the link to the page specified
    webbrowser.open(recommendation.results[0].shop, new=2)


def BuyLink2():
    webbrowser.open(recommendation.results[1].shop, new=2)


def BuyLink3():
    webbrowser.open(recommendation.results[2].shop, new=2)


# Defining the root or master of our app
app = tk.Tk()
# Changing the size of the app to 1280 x 720 so that it fits in every pc, no matter the resolution
app.geometry("1280x720+120+65")
# We set the window to not be resizable so that the image is not distorted
app.resizable(False, False)
app.title("Play It")
# Here we load all the images into PhotoImage variables
# This images are stored in the bin folder
bg = tk.PhotoImage(file="bin\Play it.png")
bg2 = tk.PhotoImage(file="bin\Inputs menu.png")
bg3 = tk.PhotoImage(file="bin\Results menu.png")
backImage = tk.PhotoImage(file="bin\Back button.png")
backImage2 = tk.PhotoImage(file="bin\Back button 2.png")
creditsImage = tk.PhotoImage(file="bin\Credits button.png")
mainbImage = tk.PhotoImage(file="bin\Main button.png")
recoImage = tk.PhotoImage(file="bin\Recommendation Button.png")
bgc = tk.PhotoImage(file="bin\Credits menu.png")
MainMenu()

app.mainloop()
