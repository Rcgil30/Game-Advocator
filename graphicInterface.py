import tkinter as tk
from tkinter import ttk

#Lists later to be used for the user selections
GenreList = []
PlatformsList = []

#Function to show the main menu to the user
def MainMenu():
    #tkinter's label is used in this case to include the background image, which is defined in the main algorithm
    bglabel = tk.Label(app, image=bg)
    bglabel.pack()
    #This button makes you switch to the next menu
    mainbutton = tk.Button(app, text="Start", width=20,
                           height=3, command=Menu2, bg="#F55A51", font=100)
    mainbutton.place(x=510, y=565)


def Menu2():
    #For loop to clear all the widgets from the root, so that we can start with the next menu
    for ele in app.winfo_children():
        ele.destroy()
    #In this canva we will show all the elements for the next menu
    canva = tk.Canvas(app)
    canva.pack()
    #Label to show the background for the second menu
    bg2label = tk.Label(canva, image=bg2)
    bg2label.pack()
    #Switch that determines if a checkbutton is selected
    swAction = tk.BooleanVar()
    #We create a button with every Genre to allow the user to click a bunch of them, so that they
    #can select multiple genres, generating then a list of genres, this will happen in the button to 
    #show the results
    ActionButton = ttk.Checkbutton(canva, text="Action", variable=swAction)
    ActionButton.place(x=190, y=250)
    swAdventure = tk.BooleanVar()
    #We build each button with the text of the Genre name and de variable that determines
    #If it is selected or not, which we'll use then to get the elements of the list
    AdventureButton = ttk.Checkbutton(
        canva, text="Adventure", variable=swAdventure)
    #With the place method, we get the buttons in a specific pixel of the window
    AdventureButton.place(x=190, y=290)
    swCoop = tk.BooleanVar()
    CoopButton = ttk.Checkbutton(canva, text="Coop", variable=swCoop)
    CoopButton.place(x=190, y=330)
    swFighting = tk.BooleanVar()
    FightingButton = ttk.Checkbutton(
        canva, text="Fighting", variable=swFighting)
    FightingButton.place(x=190, y=370)
    swFps = tk.BooleanVar()
    FpsButton = ttk.Checkbutton(canva, text="Coop", variable=swFps)
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
    SurvivalButton.place(x=190, y=570)

#Defining the root or master of our app
app = tk.Tk()
#Changing the size of the app to 1280 x 720 so that it fits in every pc, no matter the resolution
app.geometry("1280x720")
#We set the window to not be resizable so that the image is not distorted
app.resizable(False, False)
app.title("Play It")
bg = tk.PhotoImage(file="bin\Play it.png")
bg2 = tk.PhotoImage(file="bin\Inputs menu.png")
MainMenu()

app.mainloop()
