# Games Application
# Tic Tac Toe, Connect 4, Scrabble, Checkers, Chess

# wxpython used for GUI
import wx

# Used to extract game defaults from CSV files
import csv

# Used to generate random integers
from random import randint

# Used to import images
from PIL import Image

# Enables the Game Grid  and restart button, and disables the character/colour buttons and returns the character/colour they chose
def EnableGame(C1,C2,RS,Grid, user):
    C1.Disable()
    C2.Disable()
    RS.Enable()
    for children in Grid.GetChildren():
        children.GetWindow().Enable()

    return user

# Disables the Games Grid and restart button, and enables the character/colour buttons
def DisableGame(C1,C2,RS,Grid):
    C1.Enable()
    C2.Enable()
    RS.Disable()
    for children in Grid.GetChildren():
        children.GetWindow().Disable()

# Sets the button name and button bitmap accordingly when a piece is placed/moved
def PlacePiece(folder,text, window):
    if (text == ""):
        pic = wx.Bitmap(1,1)
        pic.SetMaskColour("black")
    else:
        try:
            pic = wx.Image(folder+text+".png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        except:
            pass
    window.SetBitmap(pic)
    window.SetBitmapDisabled(pic)
    window.SetName(text)

# Sets the colours for the Scrabble Board
def SetScrabColours(window):
    if (window.GetLabel() == "3W"):
        window.SetBackgroundColour("yellow")
    elif (window.GetLabel() == "2W"):
        window.SetBackgroundColour("red")
    elif (window.GetLabel() == "3L"):
        window.SetBackgroundColour("green")
    elif (window.GetLabel() == "2L"):
        window.SetBackgroundColour("blue")
    else:
        window.SetBackgroundColour("light blue")

# Extracts informations from csv file and returns it as an array
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

# Creates Home Frame where user chooses which game to play
class Home(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Board Games')
        panel = wx.Panel(self)
        home = wx.BoxSizer(wx.VERTICAL)

        # Creates buttons for each game
        TTT = wx.Button(panel, label='Tic-Tac-Toe')
        TTT.Bind(wx.EVT_BUTTON, self.pressTTT)
        home.Add(TTT, 0, wx.ALL | wx.EXPAND, 5)
        
        C4 = wx.Button(panel, label='Connect Four')
        C4.Bind(wx.EVT_BUTTON, self.pressC4)
        home.Add(C4, 0, wx.ALL | wx.EXPAND, 5)
        
        Scrab = wx.Button(panel, label='Scrabble')
        Scrab.Bind(wx.EVT_BUTTON, self.pressScrab)
        home.Add(Scrab, 0, wx.ALL | wx.EXPAND, 5)
        
        Check = wx.Button(panel, label='Checkers')
        Check.Bind(wx.EVT_BUTTON, self.pressCheck)
        home.Add(Check, 0, wx.ALL | wx.EXPAND, 5)
        
        Chess = wx.Button(panel, label='Chess')
        Chess.Bind(wx.EVT_BUTTON, self.pressChess)
        home.Add(Chess, 0, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(home)
        self.Show()

    # Displays new frame for each game when button is clicked
    def pressTTT(self, event):
        TTTFrame = TTT()
        TTTFrame.Show()

    def pressC4(self, event):
        C4Frame = C4()
        C4Frame.Show()

    def pressScrab(self, event):
        ScrabFrame = Scrab()
        ScrabFrame.Show()

    def pressCheck(self, event):
        CheckFrame = Check()
        CheckFrame.Show()

    def pressChess(self, event):
        ChessFrame = Chess()
        ChessFrame.Show()

# Creates frame for each game

# ------- Tic Tac Toe Frame -------------------------------------------------------------

class TTT(wx.Frame):
    
    def __init__(self):
        super().__init__(parent=None, title='Tic Tac Toe')
        panel = wx.Panel(self)

        # 3x3 Grid for Tic-Tac-Toe
        self.ttt = wx.GridSizer(3, 3, 0, 0)
        for i in range(0,9):
            self.ttt.Add(wx.Button(panel),0,wx.EXPAND)
        for children in self.ttt.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressttt)
            children.GetWindow().SetBackgroundColour("white")

        # Initialize user character
        self.User = ""
        
        # Allows user to choose which character to play as (O goes first, X goes second)
        self.O = wx.Button(panel, label='O')
        self.O.Bind(wx.EVT_BUTTON, self.pressO)
        self.X = wx.Button(panel, label='X')
        self.X.Bind(wx.EVT_BUTTON, self.pressX)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose O or X:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.O,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.X,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.ttt, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)           
        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.O,self.X,self.restart,self.ttt)

        # Create 2D array for board
        self.Board = []
        
        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.ttt.GetChildren():
            children.GetWindow().SetId((i+1)*10+(j+1))
            Brow.append("")
            if (j < 2):
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    # Enables grid and restart buttons when a character is chosen
    def pressO(self, event):
        self.User = EnableGame(self.O,self.X,self.restart,self.ttt,"O")

    def pressX(self, event):
        self.User = EnableGame(self.O,self.X,self.restart,self.ttt,"X")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        DisableGame(self.O,self.X,self.restart,self.ttt)
        for children in self.ttt.GetChildren():
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = ""
            PlacePiece("", "", children.GetWindow())
            
    # The button clicked is occupied by the User's character and is disabled
    def pressttt(self, event):
        self.Board[int(event.GetEventObject().GetId()/10)-1][event.GetEventObject().GetId()%10-1] = self.User
        PlacePiece("Tic-Tac-Toe/", self.User, event.GetEventObject())
        event.GetEventObject().Disable()

# --------------------------------------------------------------------------------------------

# ------------- Connect Four Frame -----------------------------------------------------------

class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four')
        panel = wx.Panel(self)

        # 6x7 grid for Connect Four
        self.c4 = wx.GridSizer(6, 7, 0, 0)
        for i in range(0,42):
            self.c4.Add(wx.Button(panel),0,wx.EXPAND)
        for children in self.c4.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressc4)
            children.GetWindow().SetBackgroundColour("medium blue")

        # Initialize user character
        self.User = ""    
        
        # Allows user to choose which colour to play as (Red goes first, Yellow goes second)
        self.Red = wx.Button(panel, label='RED')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Yellow = wx.Button(panel, label='YELLOW')
        self.Yellow.Bind(wx.EVT_BUTTON, self.pressYellow)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose RED or YELLOW:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Yellow,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.c4, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.Red,self.Yellow,self.restart,self.c4)

        # Create 2D array for board
        self.Board = []
        
        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.c4.GetChildren():
            children.GetWindow().SetId((i+1)*10+(j+1))
            Brow.append("")
            if (j < 6):
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    # Enables grid and restart buttons when a colour is chosen
    def pressRed(self, event):
        self.User = EnableGame(self.Red,self.Yellow,self.restart,self.c4,"RED")

    def pressYellow(self, event):
        self.User = EnableGame(self.Red,self.Yellow,self.restart,self.c4,"YELLOW")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        DisableGame(self.Red,self.Yellow,self.restart,self.c4)
        for children in self.c4.GetChildren():
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = ""
            PlacePiece("", "", children.GetWindow())
                
    # Places piece in the lowest available spot in the selected column
    # The column is disabled when it becomes full
    def pressc4(self, event):
        col = event.GetEventObject().GetId()%10-1
        for i in range(0,6):
            if (self.Board[i][col] == "" and (i == 5 or self.Board[i+1][col] != "")):
                for children in self.c4.GetChildren():
                    if (children.GetWindow().GetId() == (i+1)*10+(col+1)):
                        PlacePiece("Colours/", self.User, children.GetWindow())
                        self.Board[i][col] = self.User
                    if (i == 0):
                        for disable in range(0,6):
                            if (children.GetWindow().GetId() == (disable+1)*10+(col+1)):
                                children.GetWindow().Disable()

# --------------------------------------------------------------------------------------------

# ------------- Scrabble Frame ---------------------------------------------------------------

class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble')
        panel = wx.Panel(self)

        # 15x15 Grid for Scrabble
        self.scrab = wx.GridSizer(15, 15, 0, 0)
        for i in range(0,225):
            self.scrab.Add(wx.Button(panel),0,wx.EXPAND)
        for children in self.scrab.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressscrab)

        # 7x1 Grid for Letter Rack
        self.rack = wx.GridSizer(1, 7, 0, 0)
        for i in range(0,7):
            self.rack.Add(wx.Button(panel),0,wx.EXPAND)
        for children in self.rack.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressrack)
            children.GetWindow().SetBackgroundColour("tan")

        # 2nd Row (Rack, Shuffle, Play, and Solve Mode)
        row = wx.BoxSizer(wx.HORIZONTAL)
        self.Shuffle = wx.Button(panel, label='Shuffle')
        self.Shuffle.Bind(wx.EVT_BUTTON, self.pressShuffle)
        self.Play = wx.Button(panel, label='Play')
        self.Play.Bind(wx.EVT_BUTTON, self.pressPlay)
        row.Add(self.rack, 1, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Shuffle, 0, wx.ALL | wx.EXPAND)
        row.Add(self.Play, 0, wx.ALL | wx.EXPAND)
        row.Add(wx.Button(panel, label='Solve Mode'),0, wx.ALL | wx.EXPAND)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.scrab, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(row, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.Show()


        # Extract info from scrabble files
        self.board_setup = FromCSV("Scrabble/Scrabble_Board.txt")
        self.values = FromCSV("Scrabble/Scrabble_Values.txt")
        self.tiles_file = FromCSV("Scrabble/Scrabble_Tiles.txt")
        
        # Populate the bag with all tiles
        self.tiles = []
        for i in range (0,27):
            for j in range (0,int(self.tiles_file[i][1])):
                self.tiles.append(self.tiles_file[i][0])
                
        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.scrab.GetChildren():
            children.GetWindow().SetId((i+10)*100+(j+10))
            Brow.append("")
            if (j < 14):
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Fill board with multipliers
        for i in range(0,61):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]
        for children in self.scrab.GetChildren():
            children.GetWindow().SetLabel(self.Board[int(children.GetWindow().GetId()/100)-10][children.GetWindow().GetId()%100-10])
            SetScrabColours(children.GetWindow()) 

        # Initializes rack arrays
        self.rack_arr = []
        self.comp_rack_arr = []

        # Who goes first is determined by chance
        value = randint(0, 1)
        for i in range (0,2):

            # Populates both racks with tiles from the bag randomly
            # Sets ID of rack buttons to its index number
            if (i == value):
                j = 0
                for children in self.rack.GetChildren():
                    tile = randint(0,len(self.tiles)-1)
                    children.GetWindow().SetLabel(self.tiles[tile])
                    children.GetWindow().SetId(j)
                    self.rack_arr.append(self.tiles[tile])
                    del self.tiles[tile]
                    j += 1
            else:
                for j in range(0,7):
                    tile = randint(0,len(self.tiles)-1)
                    self.comp_rack_arr.append(self.tiles[tile])
                    del self.tiles[tile]

        self.click = -1
                    
    # Shuffles tiles in the rack
    def pressShuffle(self, event):
        self.click = -1
        rack = []
        for children in self.rack.GetChildren():
            rack.append(children.GetWindow().GetLabel())
        i = 0
        for children in self.rack.GetChildren():
            value = randint(0,len(rack)-1)
            children.GetWindow().SetLabel(rack[value])
            if (len(children.GetWindow().GetLabel()) == 1):
                children.GetWindow().SetBackgroundColour("tan")
            else:
                children.GetWindow().SetBackgroundColour("grey")
            self.rack_arr[i] = rack[value]
            del rack[value]
            i += 1

    # Disables tiles of the board when a word is played
    # Fills rest of rack with random remaining tiles 
    def pressPlay(self, event):
        self.click = -1
        for children in self.scrab.GetChildren():
            if (len(children.GetWindow().GetLabel()) == 1):
                children.GetWindow().Disable()
        i = 0
        for children in self.rack.GetChildren():
            if (children.GetWindow().GetLabel() == "" and len(self.tiles) > 0):
                tile = randint(0,len(self.tiles)-1)
                children.GetWindow().SetLabel(self.tiles[tile])
                children.GetWindow().SetBackgroundColour("tan")
                self.rack_arr[i] = self.tiles[tile]
                del self.tiles[tile]
            i += 1
                

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):

        self.tiles = []
        for i in range (0,27):
            for j in range (0,int(self.tiles_file[i][1])):
                self.tiles.append(self.tiles_file[i][0])

        k = 0
        for i in range(0,15):
            for j in range(0,15):
                if (k < 61 and i == int(self.board_setup[k][0]) and j == int(self.board_setup[k][1])):
                    self.Board[i][j] = self.board_setup[k][2]
                    k += 1
                else:
                    self.Board[i][j] = ""

        # Fill board with multipliers
        for children in self.scrab.GetChildren():
            children.GetWindow().Enable()
            children.GetWindow().SetLabel(self.Board[int(children.GetWindow().GetId()/100)-10][children.GetWindow().GetId()%100-10])
            SetScrabColours(children.GetWindow())

        # Who goes first is determined by chance
        value = randint(0, 1)
        for i in range (0,2):

            # Populates both racks with tiles from the bag randomly
            if (i == value):
                j = 0
                for children in self.rack.GetChildren():
                    tile = randint(0,len(self.tiles)-1)
                    children.GetWindow().SetLabel(self.tiles[tile])
                    children.GetWindow().SetBackgroundColour("tan")
                    self.rack_arr[j] = self.tiles[tile]
                    del self.tiles[tile]
                    j += 1
            else:
                for j in range(0,7):
                    tile = randint(0,len(self.tiles)-1)
                    self.comp_rack_arr[j] = self.tiles[tile]
                    del self.tiles[tile]

    # Places the piece that was chosen onto an empty space on the board
    def pressscrab(self, event):
        if (len(event.GetEventObject().GetLabel()) == 1):
            empty = False
            for children in self.rack.GetChildren():
                if (empty == False):
                    if (children.GetWindow().GetLabel() == ""):
                        empty = True
                        children.GetWindow().SetLabel(event.GetEventObject().GetLabel())
                        children.GetWindow().SetBackgroundColour("tan")
            event.GetEventObject().SetLabel(self.Board[int(event.GetEventObject().GetId()/100)-10][event.GetEventObject().GetId()%100-10])
            SetScrabColours(event.GetEventObject())
        else:
            if (self.click >= 0):
                event.GetEventObject().SetLabel(self.rack_arr[self.click])
                event.GetEventObject().SetBackgroundColour("tan")
                for children in self.rack.GetChildren():
                    if (children.GetWindow().GetId() == self.click):
                        children.GetWindow().SetLabel("")
                        children.GetWindow().SetBackgroundColour("grey")
                self.click = -1

    # Chooses a piece from the rack to place
    def pressrack(self, event):
        if (event.GetEventObject().GetLabel() != ""):
            self.click = event.GetEventObject().GetId()
        else:
            self.click = -1

# --------------------------------------------------------------------------------------------

# ------------- Checkers Frame ---------------------------------------------------------------

class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers')
        panel = wx.Panel(self)

        # 8x8 Grid for Checkers
        self.check = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            self.check.Add(wx.Button(panel),0,wx.EXPAND)    
        # Colours board according to checkers board layout
        i = 1
        switch = 0
        for children in self.check.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.presscheck)
            if (i%2 == switch):
                children.GetWindow().SetBackgroundColour("tan")
            else:
                children.GetWindow().SetBackgroundColour("wheat")
            if (i%8 == 0):
                switch = 1-switch
            i += 1

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (Red goes first, Black goes second)
        self.Red = wx.Button(panel, label='RED')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Black = wx.Button(panel, label='BLACK')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose RED or BLACK:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.check, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.Red,self.Black,self.restart,self.check)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("Checkers/Checkers_Board.txt")
                
        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.check.GetChildren():
            children.GetWindow().SetId((i+1)*10+(j+1))
            Brow.append("")
            if (j < 7):
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Places pieces on the board as if the user is 'RED'
        for i in range(0,24):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]

        self.click = 0
        
    # Enables grid and restart buttons when a character is chosen
    def pressRed(self, event):
        self.User = EnableGame(self.Red,self.Black,self.restart,self.check,"RED")

        # Sets up the board with pieces
        for children in self.check.GetChildren():
            PlacePiece("Colours/", self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1], children.GetWindow())

    def pressBlack(self, event):
        self.User = EnableGame(self.Red,self.Black,self.restart,self.check,"BLACK")

        # Sets up the board with pieces
        # Swaps Red abd Black pieces

        for children in self.check.GetChildren():
            PlacePiece("Colours/", self.Board[7-(int(children.GetWindow().GetId()/10)-1)][7-(children.GetWindow().GetId()%10-1)], children.GetWindow())
        for children in self.check.GetChildren():          
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = children.GetWindow().GetName()

    # Resets board to the setup before the character is chosen 
    def pressRS(self, event):
        self.click = 0
        DisableGame(self.Red,self.Black,self.restart,self.check)
        for children in self.check.GetChildren():
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = ""
            PlacePiece("", "", children.GetWindow())
        for i in range(0,24):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]

    # Moves selected piece to where the user clicks next
    def presscheck(self, event):

        # First click establishes which piece the user wants to move
        if (self.click == 0):
            if (event.GetEventObject().GetName()[0:5] == self.User):
                self.click = event.GetEventObject().GetId()
                
        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if (event.GetEventObject().GetName()[0:5] != self.User):
                PlacePiece("Colours/", self.Board[int(self.click/10)-1][self.click%10-1], event.GetEventObject())
                self.Board[int(event.GetEventObject().GetId()/10)-1][event.GetEventObject().GetId()%10-1] = self.Board[int(self.click/10)-1][self.click%10-1]
                self.Board[int(self.click/10)-1][self.click%10-1] = ""
                for children in self.check.GetChildren():
                    if (children.GetWindow().GetId() == self.click):
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
            else:
                self.click = event.GetEventObject().GetId()

# --------------------------------------------------------------------------------------------

# ------------- Chess Frame ------------------------------------------------------------------

class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess')
        panel = wx.Panel(self)

        # 8x8 Grid for Chess
        self.chess = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            self.chess.Add(wx.Button(panel),0,wx.EXPAND)

        # Colours board according to chess board layout
        i = 1
        switch = 0
        for children in self.chess.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.presschess)
            if (i%2 == switch):
                children.GetWindow().SetBackgroundColour("tan")
            else:
                children.GetWindow().SetBackgroundColour("wheat")
            if (i%8 == 0):
                switch = 1-switch
            i += 1

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (White goes first, Black goes second)
        self.White = wx.Button(panel, label='WHITE')
        self.White.Bind(wx.EVT_BUTTON, self.pressWhite)
        self.Black = wx.Button(panel, label='BLACK')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose WHITE or BLACK:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.White,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        # Adds all buttons to frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.chess, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.White,self.Black,self.restart,self.chess)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("Chess/Chess_Board.txt")
                
        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.chess.GetChildren():
            children.GetWindow().SetId((i+1)*10+(j+1))
            Brow.append("")
            if (j < 7):
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Sets up pieces as if user is 'WHITE'
        for i in range(0,32):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]+"_"+self.board_setup[i][3]

        self.click = 0
        
    # Enables grid and restart buttons when a character is chosen
    def pressWhite(self, event):
        self.User = EnableGame(self.White,self.Black,self.restart,self.chess,"WHITE")

        # Sets up the board with pieces
        for children in self.chess.GetChildren():
            PlacePiece("Chess/", self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1], children.GetWindow())

    def pressBlack(self, event):
        self.User = EnableGame(self.White,self.Black,self.restart,self.chess,"BLACK")

        # Sets up the board with pieces
        # Swaps White abd Black pieces
        for children in self.chess.GetChildren():
            PlacePiece("Chess/", self.Board[7-(int(children.GetWindow().GetId()/10)-1)][7-(children.GetWindow().GetId()%10-1)], children.GetWindow())
        for children in self.chess.GetChildren():          
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = children.GetWindow().GetName()

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        self.click = 0
        DisableGame(self.White,self.Black,self.restart,self.chess)
        for children in self.chess.GetChildren():
            self.Board[int(children.GetWindow().GetId()/10)-1][children.GetWindow().GetId()%10-1] = ""
            PlacePiece("", "", children.GetWindow())
        for i in range(0,32):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]+"_"+self.board_setup[i][3]

    # Places selected piece to where the user clicks next
    def presschess(self, event):

        # First click establishes which piece the user wants to move
        if (self.click == 0):
            if (event.GetEventObject().GetName()[0:5] == self.User):
                self.click = event.GetEventObject().GetId()
                
        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if (event.GetEventObject().GetName()[0:5] != self.User):
                PlacePiece("Chess/", self.Board[int(self.click/10)-1][self.click%10-1], event.GetEventObject())
                self.Board[int(event.GetEventObject().GetId()/10)-1][event.GetEventObject().GetId()%10-1] = self.Board[int(self.click/10)-1][self.click%10-1]
                self.Board[int(self.click/10)-1][self.click%10-1] = ""
                for children in self.chess.GetChildren():
                    if (children.GetWindow().GetId() == self.click):
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
            else:
                self.click = event.GetEventObject().GetId()   

# --------------------------------------------------------------------------------------------

# Runs Application
if __name__ == '__main__':
    app = wx.App()
    frame = Home()
    app.MainLoop()
    
