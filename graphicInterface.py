import tkinter as tk
from tkinter import ttk

GenreList = []


def MainMenu():
    bglabel = tk.Label(app, image=bg)
    bglabel.pack()
    mainbutton = tk.Button(app, text="Start", width=20,
                           height=3, command=Menu2, bg="#F55A51", font=100)
    mainbutton.place(x=510, y=565)


def Menu2():
    for ele in app.winfo_children():
        ele.destroy()
    canva = tk.Canvas(app)
    canva.pack()
    bg2label = tk.Label(canva, image=bg2)
    bg2label.pack()
    # Switch que nos determina si el género está seleccionado
    swAction = tk.BooleanVar()
    ActionButton = ttk.Checkbutton(canva, text="Action", variable=swAction)
    ActionButton.place(x=190, y=250)
    swAdventure = tk.BooleanVar()
    AdventureButton = ttk.Checkbutton(
        canva, text="Adventure", variable=swAdventure)
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


app = tk.Tk()
app.geometry("1280x720")
app.resizable(False, False)
app.title("Game Advocator")
bg = tk.PhotoImage(file="bin\Play it.png")
bg2 = tk.PhotoImage(file="bin\Inputs menu.png")
MainMenu()

app.mainloop()
