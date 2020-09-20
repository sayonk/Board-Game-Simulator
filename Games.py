# Functions for all games

# wxpython used for GUI
import wx

# Used to extract game defaults from CSV files
import csv


# Enables the Game Grid  and restart button, and disables the character/colour buttons and returns the
# character/colour they chose

def EnableGame(C1, C2, RS, Grid, user):
    C1.Disable()
    C2.Disable()
    RS.SetLabel("Restart Game")
    for children in Grid.GetChildren():
        children.GetWindow().Enable()

    return user


# Disables the Games Grid and restart button, and enables the character/colour buttons
def DisableGame(C1, C2, RS, Grid):
    C1.Enable()
    C2.Enable()
    RS.SetLabel("Start Game")
    for children in Grid.GetChildren():
        children.GetWindow().Disable()


# Sets the button name and button bitmap accordingly when a piece is placed/moved
def PlacePiece(folder, text, window):
    if text == "":
        pic = wx.Bitmap(1, 1)
        pic.SetMaskColour("black")
    else:
        pic = wx.Image(folder + text + ".png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    window.SetBitmap(pic)
    window.SetBitmapDisabled(pic)
    window.SetName(text)


# Extracts information from csv file and returns it as an array
def FromCSV(file):
    array = []
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array.append(row)
    except IOError:
        pass
    return array


