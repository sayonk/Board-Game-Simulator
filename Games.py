# Games Application
# Tic Tac Toe, Connect 4, Scrabble, Checkers, Chess

# wxpython used for GUI
import wx

# Used to extract game defaults from CSV files
import csv

# Used to generate random integers
from random import randint


# Enables the Game Grid  and restart button, and disables the character/colour buttons and returns the
# character/colour they chose
def EnableGame(C1, C2, RS, Grid, user):
    C1.Disable()
    C2.Disable()
    RS.Enable()
    for children in Grid.GetChildren():
        children.GetWindow().Enable()

    return user


# Disables the Games Grid and restart button, and enables the character/colour buttons
def DisableGame(C1, C2, RS, Grid):
    C1.Enable()
    C2.Enable()
    RS.Disable()
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


# Sets the colours for the Scrabble Board
def SetScrabColours(window):
    if window.GetLabel() == "3W":
        window.SetBackgroundColour("yellow")
    elif window.GetLabel() == "2W":
        window.SetBackgroundColour("red")
    elif window.GetLabel() == "3L":
        window.SetBackgroundColour("green")
    elif window.GetLabel() == "2L":
        window.SetBackgroundColour("blue")
    else:
        window.SetBackgroundColour("light blue")


# Gets an array of valid checkers moves given the location of the piece chosen
def getValidCheckMoves(row, col, user, board):

    if user == "RED":
        opp = "BLACK"
    else:
        opp = "RED"

    arr = []

    # Checks whether the piece can go to a space diagonally
    for i in range(-1,2):
        if i != 0:
            if row > 0 and 0 <= col+i <= 7 and board[row - 1][col + i] == "":
                arr.append([row - 1, col + i])
            elif row > 1 and 0 <= col+2*i <= 7 and board[row - 2][col + 2*i] == "" and board[row - 1][col + i] == "":
                arr.append([row - 2, col + 2*i])
    return arr


# Gets an array of valid chess moves given the location of the piece chosen
def getValidChessMoves(row, col, user, board, pMoved):

    arr = []
    piece = board[row][col][6:]

    if user == "WHITE":
        opp = "BLACK"
    else:
        opp = "WHITE"

    # If the pawn hasn't moved, it can move 2 up, otherwise only 1 up
    if piece == "PAWN":
        if row > 0 and board[row-1][col] == "":
            arr.append([row-1,col])
        for i in range(-1, 2):
            if i != 0:
                if row > 0 and 0 <= col+i <= 7 and board[row-1][col+i][:5] == opp:
                    arr.append([row-1][col-1])
        if not pMoved:
            arr.append([row-2,col])

    # Checks each spot where the knight is an 'L shape' away from
    elif piece == "KNIGHT":
        for i in range(8):
            rowK = (-2*(int(i/2)%2)+1)*(i%2+1)
            colK = ((i+1)%2+1)*(1-2*int(i/4))
            if 0 <= row+rowK <= 7 and 0 <= col+colK <= 7 and board[row+int(rowK)][col+int(colK)][:5] != user:
                arr.append([row+int(rowK),col+int(colK)])

    # Checks every spot where the piece can go based on their abilities
    else:
        if piece == "BISHOP" or piece == "ROOK":
            rng = 4
        else:
            rng = 8
        for i in range(rng):

            # Set formulas for each piece's abilities that can be calculated from the index number of the loop
            if piece == "BISHOP":
                rowP = -2*(i%2)+1
                colP = -2*int(i/2)+1
            elif piece == "ROOK":
                rowP = (i%2)*(i-2)
                colP = (1-i%2)*(i-1)
            else:
                rowP = (-2*(i%2)+1)*int(bool(i%7))
                colP = int((i+3)/2)-3-int((int((i+3)/2)-3)/2)

            # A piece cannot go any further if another piece is in the way
            blocked = False
            while not blocked:
                if 0 <= row+rowP <= 7 and 0 <= col+colP <= 7 and board[row+int(rowP)][col+int(colP)][:5] != user:
                    arr.append([row+int(rowP),col+int(colP)])
                    if board[row+int(rowP)][col+int(colP)][:5] == opp:
                        blocked = True
                else:
                    blocked = True
                if rowP != 0:
                    rowP += abs(rowP)/rowP
                if colP != 0:
                    colP += abs(colP)/colP
                if piece == "KING":
                    blocked = True
    return arr

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


# Displays new frame for each game when button is clicked
def pressTTT(self):
    TTTFrame = TTT()
    TTTFrame.Show()


def pressC4(self):
    C4Frame = C4()
    C4Frame.Show()


def pressScrab(self):
    ScrabFrame = Scrab()
    ScrabFrame.Show()


def pressCheck(self):
    CheckFrame = Check()
    CheckFrame.Show()


def pressChess(self):
    ChessFrame = Chess()
    ChessFrame.Show()


# Creates Home Frame where user chooses which game to play
class Home(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Board Games', size=(300, 300))
        panel = wx.Panel(self)
        home = wx.BoxSizer(wx.VERTICAL)

        # Creates buttons for each game
        btnTTT = wx.Button(panel, label='Tic-Tac-Toe')
        btnTTT.Bind(wx.EVT_BUTTON, pressTTT)
        btnTTT.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnTTT.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnTTT, 0, wx.ALL | wx.EXPAND, 5)

        btnC4 = wx.Button(panel, label='Connect Four')
        btnC4.Bind(wx.EVT_BUTTON, pressC4)
        btnC4.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnC4.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnC4, 0, wx.ALL | wx.EXPAND, 5)

        btnScrab = wx.Button(panel, label='Scrabble')
        btnScrab.Bind(wx.EVT_BUTTON, pressScrab)
        btnScrab.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnScrab.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnScrab, 0, wx.ALL | wx.EXPAND, 5)

        btnCheck = wx.Button(panel, label='Checkers')
        btnCheck.Bind(wx.EVT_BUTTON, pressCheck)
        btnCheck.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnCheck.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnCheck, 0, wx.ALL | wx.EXPAND, 5)

        btnChess = wx.Button(panel, label='Chess')
        btnChess.Bind(wx.EVT_BUTTON, pressChess)
        btnChess.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnChess.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnChess, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(home)
        self.CreateStatusBar()
        self.Show()

    def OnMouseEnter(self, event):
        self.StatusBar.SetStatusText("Click to open game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# Creates frame for each game

# ------- Tic Tac Toe Frame -------------------------------------------------------------


class TTT(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Tic Tac Toe')
        panel = wx.Panel(self)

        # 3x3 Grid for Tic-Tac-Toe
        self.ttt = wx.GridSizer(3, 3, 0, 0)
        for i in range(0, 9):
            self.ttt.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.ttt.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnTTT)
            children.GetWindow().SetBackgroundColour("white")

        # Initialize user character
        self.User = ""

        # Allows user to choose which character to play as (O goes first, X goes second)
        self.O = wx.Button(panel, label='O')
        self.O.Bind(wx.EVT_BUTTON, self.pressO)
        self.O.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.O.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.X = wx.Button(panel, label='X')
        self.X.Bind(wx.EVT_BUTTON, self.pressX)
        self.X.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.X.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose O or X:'), 1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.O, 0, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.X, 0, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        self.solve = wx.Button(panel, label='Solve Mode')
        self.solve.Bind(wx.EVT_BUTTON, self.pressSolve)
        self.solve.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.solve.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose.Add(self.solve, 0, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)
        self.restart.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.restart.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.ttt, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.O, self.X, self.restart, self.ttt)

        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.ttt.GetChildren():
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 2:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    # Enables grid and restart buttons when a character is chosen
    def pressO(self, event):
        self.User = EnableGame(self.O, self.X, self.restart, self.ttt, "O")

    def pressX(self, event):
        self.User = EnableGame(self.O, self.X, self.restart, self.ttt, "X")

    def pressSolve(self, event):
        print("You are now in Solve Mode")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        DisableGame(self.O, self.X, self.restart, self.ttt)
        for children in self.ttt.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
            PlacePiece("", "", children.GetWindow())

    # The button clicked is occupied by the User's character and is disabled
    def btnTTT(self, event):
        self.Board[int(event.GetEventObject().GetId() / 10) - 1][event.GetEventObject().GetId() % 10 - 1] = self.User
        PlacePiece("Tic-Tac-Toe/", self.User, event.GetEventObject())
        event.GetEventObject().Disable()

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.solve:
            self.StatusBar.SetStatusText("Calculate the best possible move")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# --------------------------------------------------------------------------------------------

# ------------- Connect Four Frame -----------------------------------------------------------

class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four', size=(500, 500))
        panel = wx.Panel(self)

        # 6x7 grid for Connect Four
        self.c4 = wx.GridSizer(6, 7, 0, 0)
        for i in range(0, 42):
            self.c4.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.c4.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnC4)
            children.GetWindow().SetBackgroundColour("medium blue")

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (Red goes first, Yellow goes second)
        self.Red = wx.Button(panel, label='RED')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Red.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Red.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Yellow = wx.Button(panel, label='YELLOW')
        self.Yellow.Bind(wx.EVT_BUTTON, self.pressYellow)
        self.Yellow.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Yellow.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose RED or YELLOW:'), 1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red, 0, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Yellow, 0, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        self.solve = wx.Button(panel, label='Solve Mode')
        self.solve.Bind(wx.EVT_BUTTON, self.pressSolve)
        self.solve.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.solve.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose.Add(self.solve, 0, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)
        self.restart.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.restart.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.c4, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.Red, self.Yellow, self.restart, self.c4)

        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.c4.GetChildren():
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 6:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    # Enables grid and restart buttons when a colour is chosen
    def pressRed(self, event):
        self.User = EnableGame(self.Red, self.Yellow, self.restart, self.c4, "RED")

    def pressYellow(self, event):
        self.User = EnableGame(self.Red, self.Yellow, self.restart, self.c4, "YELLOW")

    def pressSolve(self, event):
        print("You are now in Solve Mode")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        DisableGame(self.Red, self.Yellow, self.restart, self.c4)
        for children in self.c4.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
            PlacePiece("", "", children.GetWindow())

    # Places piece in the lowest available spot in the selected column
    # The column is disabled when it becomes full
    def btnC4(self, event):
        col = event.GetEventObject().GetId() % 10 - 1
        for i in range(0, 6):
            if self.Board[i][col] == "" and (i == 5 or self.Board[i + 1][col] != ""):
                for children in self.c4.GetChildren():
                    if children.GetWindow().GetId() == (i + 1) * 10 + (col + 1):
                        PlacePiece("Colours/", self.User, children.GetWindow())
                        self.Board[i][col] = self.User
                    if i == 0:
                        for disable in range(0, 6):
                            if children.GetWindow().GetId() == (disable + 1) * 10 + (col + 1):
                                children.GetWindow().Disable()

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.solve:
            self.StatusBar.SetStatusText("Calculate the best possible move")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# --------------------------------------------------------------------------------------------

# ------------- Scrabble Frame ---------------------------------------------------------------

class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble', size=(600, 650))
        panel = wx.Panel(self)

        # 15x15 Grid for Scrabble
        self.scrab = wx.GridSizer(15, 15, 0, 0)
        for i in range(0, 225):
            self.scrab.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.scrab.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnScrab)

        # 7x1 Grid for Letter Rack
        self.rack = wx.GridSizer(1, 7, 0, 0)
        for i in range(0, 7):
            self.rack.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.rack.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressrack)
            children.GetWindow().SetBackgroundColour("tan")

        # 2nd Row (Rack, Shuffle, Play, and Solve Mode)
        row = wx.BoxSizer(wx.HORIZONTAL)
        self.Shuffle = wx.Button(panel, label='Shuffle')
        self.Shuffle.Bind(wx.EVT_BUTTON, self.pressShuffle)
        self.Shuffle.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Shuffle.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Play = wx.Button(panel, label='Play')
        self.Play.Bind(wx.EVT_BUTTON, self.pressPlay)
        self.Play.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Play.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.solve = wx.Button(panel, label='Solve Mode')
        self.solve.Bind(wx.EVT_BUTTON, self.pressSolve)
        self.solve.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.solve.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        row.Add(self.rack, 1, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Shuffle, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Play, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.solve, 0, wx.ALL | wx.EXPAND, 5)

        # Disable Play button (Only gets enabled when a valid word is on the board)
        self.Play.Disable()

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)
        self.restart.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.restart.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.scrab, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(row, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        # Extract info from scrabble files
        self.board_setup = FromCSV("Scrabble/Scrabble_Board.txt")
        self.values = FromCSV("Scrabble/Scrabble_Values.txt")
        self.tiles_file = FromCSV("Scrabble/Scrabble_Tiles.txt")
        self.dictionary = FromCSV("Scrabble/Scrabble_Dictionary.txt")

        # Populate the bag with all tiles
        self.tiles = []
        for i in range(0, 27):
            for j in range(0, int(self.tiles_file[i][1])):
                self.tiles.append(self.tiles_file[i][0])

        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.scrab.GetChildren():
            children.GetWindow().SetId((i + 10) * 100 + (j + 10))
            Brow.append("")
            if j < 14:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Fill board with multipliers
        for i in range(0, 61):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]
        multipliers = 0
        for children in self.scrab.GetChildren():
            children.GetWindow().SetLabel(
                self.Board[int(children.GetWindow().GetId() / 100) - 10][children.GetWindow().GetId() % 100 - 10])
            SetScrabColours(children.GetWindow())

        # Initializes rack arrays
        self.rack_arr = []
        self.comp_rack_arr = []

        # Who goes first is determined by chance
        value = randint(0, 1)
        for i in range(0, 2):

            # Populates both racks with tiles from the bag randomly
            # Sets ID of rack buttons to its index number
            if i == value:
                j = 0
                for children in self.rack.GetChildren():
                    tile = randint(0, len(self.tiles) - 1)
                    children.GetWindow().SetLabel(self.tiles[tile])
                    children.GetWindow().SetId(j)
                    self.rack_arr.append(self.tiles[tile])
                    del self.tiles[tile]
                    j += 1
            else:
                for j in range(0, 7):
                    tile = randint(0, len(self.tiles) - 1)
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
            value = randint(0, len(rack) - 1)
            children.GetWindow().SetLabel(rack[value])
            if len(children.GetWindow().GetLabel()) == 1:
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
            if len(children.GetWindow().GetLabel()) == 1 and children.GetWindow().IsEnabled():
                self.Board[int(children.GetWindow().GetId() / 100) - 10][children.GetWindow().GetId() % 100 - 10] \
                    = children.GetWindow().GetLabel()
                children.GetWindow().Disable()
        i = 0
        for children in self.rack.GetChildren():
            if children.GetWindow().GetLabel() == "" and len(self.tiles) > 0:
                tile = randint(0, len(self.tiles) - 1)
                children.GetWindow().SetLabel(self.tiles[tile])
                children.GetWindow().SetBackgroundColour("tan")
                self.rack_arr[i] = self.tiles[tile]
                del self.tiles[tile]
            i += 1

        # Disable Play button again after word has been played
        self.Play.Disable()

    def pressSolve(self, event):
        print("You are now in Solve Mode")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):

        self.click = -1
        self.tiles = []
        for i in range(0, 27):
            for j in range(0, int(self.tiles_file[i][1])):
                self.tiles.append(self.tiles_file[i][0])

        k = 0
        for i in range(0, 15):
            for j in range(0, 15):
                if k < 61 and i == int(self.board_setup[k][0]) and j == int(self.board_setup[k][1]):
                    self.Board[i][j] = self.board_setup[k][2]
                    k += 1
                else:
                    self.Board[i][j] = ""

        # Fill board with multipliers
        for children in self.scrab.GetChildren():
            children.GetWindow().Enable()
            children.GetWindow().SetLabel(
                self.Board[int(children.GetWindow().GetId() / 100) - 10][children.GetWindow().GetId() % 100 - 10])
            SetScrabColours(children.GetWindow())

        # Who goes first is determined by chance
        value = randint(0, 1)
        for i in range(0, 2):

            # Populates both racks with tiles from the bag randomly
            if i == value:
                j = 0
                for children in self.rack.GetChildren():
                    tile = randint(0, len(self.tiles) - 1)
                    children.GetWindow().SetLabel(self.tiles[tile])
                    children.GetWindow().SetBackgroundColour("tan")
                    self.rack_arr[j] = self.tiles[tile]
                    del self.tiles[tile]
                    j += 1
            else:
                for j in range(0, 7):
                    tile = randint(0, len(self.tiles) - 1)
                    self.comp_rack_arr[j] = self.tiles[tile]
                    del self.tiles[tile]

    # Places the piece that was chosen onto an empty space on the board
    def btnScrab(self, event):

        # Places piece back on rack if its clicked while on the board
        if len(event.GetEventObject().GetLabel()) == 1:
            empty = False
            i = 0
            for children in self.rack.GetChildren():
                if not empty:
                    if children.GetWindow().GetLabel() == "":
                        empty = True
                        children.GetWindow().SetLabel(event.GetEventObject().GetLabel())
                        children.GetWindow().SetBackgroundColour("tan")
                        self.rack_arr[i] = event.GetEventObject().GetLabel()
                i += 1
            event.GetEventObject().SetLabel(self.Board[int(event.GetEventObject().GetId() / 100) - 10]
                                            [event.GetEventObject().GetId() % 100 - 10])
            SetScrabColours(event.GetEventObject())
        elif self.click >= 0:

            event.GetEventObject().SetLabel(self.rack_arr[self.click])
            event.GetEventObject().SetBackgroundColour("tan")

            i = 0
            for children in self.rack.GetChildren():
                if children.GetWindow().GetId() == self.click:
                    children.GetWindow().SetLabel("")
                    children.GetWindow().SetBackgroundColour("grey")
                    self.rack_arr[i] = ""
                i += 1
            self.click = -1

        # Check if new tiles on the board are in line
        words = []
        vwords = ["","","","","","","","","","","","","","",""]
        hword = ""
        rowIDs = []
        colIDs = []
        new_tiles = []
        count_new = 0
        tiles_between = 0
        touchCheck = False
        centerFilled = False
        for children in self.scrab.GetChildren():
            childRowID = int(children.GetWindow().GetId() / 100) - 10
            childColID = children.GetWindow().GetId() % 100 - 10
            if len(children.GetWindow().GetLabel()) == 1:
                hword += children.GetWindow().GetLabel()
                vwords[childColID] += children.GetWindow().GetLabel()
                if count_new > 0:
                    tiles_between += 1
                    rowIDs.append(childRowID)
                    colIDs.append(childColID)
                # Ends the word if the string goes until the end of the board
                if childColID == 14:
                    if len(hword) > 1:
                        words.append(hword)
                    hword = ""
                if childRowID == 14:
                    if len(vwords[childColID]) > 1:
                        words.append(vwords[childColID])
                    vwords[childColID] = ""
                if children.GetWindow().IsEnabled():
                    if children.GetWindow().GetId() == 1717:
                        centerFilled = True
                    new_tiles.append(tiles_between)
                    if count_new == 0:
                        rowIDs.append(childRowID)
                        colIDs.append(childColID)

                    # Checks if any tile is touching an already played tile
                    if len(self.Board[7][7]) == 1:  # Center box is always filled on the first move
                        if childRowID < 14 and len(self.Board[childRowID + 1][childColID]) == 1:
                            touchCheck = True
                        if childRowID > 0 and len(self.Board[childRowID - 1][childColID]) == 1:
                            touchCheck = True
                        if childColID < 14 and len(self.Board[childRowID][childColID + 1]) == 1:
                            touchCheck = True
                        if childColID > 0 and len(self.Board[childRowID][childColID - 1]) == 1:
                            touchCheck = True

                    elif count_new > 0 and centerFilled:
                        touchCheck = True

                    count_new += 1
            else:
                if len(hword) > 1:
                    words.append(hword)
                if len(vwords[childColID]) > 1:
                    words.append(vwords[childColID])
                hword = ""
                vwords[childColID] = ""

        # Checks if the played tiles are in line
        check = True
        if touchCheck:
            if len(new_tiles) > 1:
                direction = "NEITHER"
                rowID = rowIDs[new_tiles[0]]
                colID = colIDs[new_tiles[0]]
                for item in new_tiles:
                    if rowIDs[item] != rowID:
                        check = False
                if not check:
                    check = True
                    for item in new_tiles:
                        if colIDs[item] != colID:
                            check = False
                    if check:
                        direction = "VERTICAL"
                else:
                    direction = "HORIZONTAL"
                if check:
                    if direction == "HORIZONTAL":
                        i = 1
                        j = 1
                        while i < new_tiles[-1]+1:
                            if rowIDs[i] == rowID:
                                if colIDs[i] != colID + j:
                                    check = False
                                j += 1
                            i += 1
                    else:
                        i = 1
                        j = 1
                        while i < new_tiles[-1]+1:
                            if colIDs[i] == colID:
                                if rowIDs[i] != rowID + j:
                                    check = False
                                j += 1
                            i += 1

        # Checks if all played words are in the scrabble dictionary
        wordCheck = True
        for item in words:
            if [item.lower()] not in self.dictionary:
                wordCheck = False

        if touchCheck and check and wordCheck:
            self.Play.Enable()
        else:
            self.Play.Disable()

    # Chooses a piece from the rack to place
    def pressrack(self, event):
        if event.GetEventObject().GetLabel() != "":
            self.click = event.GetEventObject().GetId()
        else:
            self.click = -1

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.solve:
            self.StatusBar.SetStatusText("Calculate the best possible move")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        elif event.GetEventObject() == self.Shuffle:
            self.StatusBar.SetStatusText("Shuffle the tiles in your rack")
        elif event.GetEventObject() == self.Play:
            self.StatusBar.SetStatusText("Play the new word onto the board")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# --------------------------------------------------------------------------------------------

# ------------- Checkers Frame ---------------------------------------------------------------

class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers', size=(500, 550))
        panel = wx.Panel(self)

        # 8x8 Grid for Checkers
        self.check = wx.GridSizer(8, 8, 0, 0)
        for i in range(0, 64):
            self.check.Add(wx.Button(panel), 0, wx.EXPAND)
            # Colours board according to checkers board layout
        i = 1
        switch = 0
        for children in self.check.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnCheck)
            if i % 2 == switch:
                children.GetWindow().SetBackgroundColour("tan")
            else:
                children.GetWindow().SetBackgroundColour("wheat")
            if i % 8 == 0:
                switch = 1 - switch
            i += 1

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (Red goes first, Black goes second)
        self.Red = wx.Button(panel, label='RED')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Red.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Red.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Black = wx.Button(panel, label='BLACK')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        self.Black.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Black.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose RED or BLACK:'), 1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red, 0, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black, 0, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        self.solve = wx.Button(panel, label='Solve Mode')
        self.solve.Bind(wx.EVT_BUTTON, self.pressSolve)
        self.solve.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.solve.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose.Add(self.solve, 0, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)
        self.restart.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.restart.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.check, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.Red, self.Black, self.restart, self.check)

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
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 7:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Places pieces on the board as if the user is 'RED'
        for i in range(0, 24):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]

        self.click = 0
        self.validMoves = []

    # Enables grid and restart buttons when a character is chosen
    def pressRed(self, event):
        self.User = EnableGame(self.Red, self.Black, self.restart, self.check, "RED")

        # Sets up the board with pieces
        for children in self.check.GetChildren():
            PlacePiece("Colours/",
                       self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1],
                       children.GetWindow())

    def pressBlack(self, event):
        self.User = EnableGame(self.Red, self.Black, self.restart, self.check, "BLACK")

        # Sets up the board with pieces
        # Swaps Red abd Black pieces

        for children in self.check.GetChildren():
            PlacePiece("Colours/", self.Board[7 - (int(children.GetWindow().GetId() / 10) - 1)][
                7 - (children.GetWindow().GetId() % 10 - 1)], children.GetWindow())
        for children in self.check.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][
                children.GetWindow().GetId() % 10 - 1] = children.GetWindow().GetName()

    def pressSolve(self, event):
        print("You are now in Solve Mode")

    # Resets board to the setup before the character is chosen 
    def pressRS(self, event):
        self.click = 0
        self.validMoves = []
        DisableGame(self.Red, self.Black, self.restart, self.check)
        for children in self.check.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
            PlacePiece("", "", children.GetWindow())
        for i in range(0, 24):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]

    # Moves selected piece to where the user clicks next
    def btnCheck(self, event):

        rowID = int(event.GetEventObject().GetId() / 10) - 1
        colID = event.GetEventObject().GetId() % 10 - 1

        # First click establishes which piece the user wants to move
        if self.click == 0:
            if event.GetEventObject().GetName() == self.User:
                self.click = event.GetEventObject().GetId()
                self.validMoves = getValidCheckMoves(rowID, colID, self.User, self.Board)

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if [rowID,colID] in self.validMoves:
                PlacePiece("Colours/", self.Board[int(self.click / 10) - 1][self.click % 10 - 1],
                           event.GetEventObject())
                self.Board[int(event.GetEventObject().GetId() / 10) - 1][event.GetEventObject().GetId() % 10 - 1] = \
                    self.Board[int(self.click / 10) - 1][self.click % 10 - 1]
                self.Board[int(self.click / 10) - 1][self.click % 10 - 1] = ""
                for children in self.check.GetChildren():
                    if children.GetWindow().GetId() == self.click:
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
                self.validMoves = []
            else:
                self.click = event.GetEventObject().GetId()
                self.validMoves = getValidCheckMoves(rowID, colID, self.User, self.Board)

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.solve:
            self.StatusBar.SetStatusText("Calculate the best possible move")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# --------------------------------------------------------------------------------------------

# ------------- Chess Frame ------------------------------------------------------------------

class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess', size=(500, 550))
        panel = wx.Panel(self)

        # 8x8 Grid for Chess
        self.chess = wx.GridSizer(8, 8, 0, 0)
        for i in range(0, 64):
            self.chess.Add(wx.Button(panel), 0, wx.EXPAND)

        # Colours board according to chess board layout
        i = 1
        switch = 0
        for children in self.chess.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnChess)
            if i % 2 == switch:
                children.GetWindow().SetBackgroundColour("tan")
            else:
                children.GetWindow().SetBackgroundColour("wheat")
            if i % 8 == 0:
                switch = 1 - switch
            i += 1

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (White goes first, Black goes second)
        self.White = wx.Button(panel, label='WHITE')
        self.White.Bind(wx.EVT_BUTTON, self.pressWhite)
        self.White.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.White.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Black = wx.Button(panel, label='BLACK')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        self.Black.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Black.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose WHITE or BLACK:'), 1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.White, 0, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black, 0, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        self.solve = wx.Button(panel, label='Solve Mode')
        self.solve.Bind(wx.EVT_BUTTON, self.pressSolve)
        self.solve.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.solve.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose.Add(self.solve, 0, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)
        self.restart.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.restart.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        # Adds all buttons to frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.chess, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.White, self.Black, self.restart, self.chess)

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
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 7:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

        # Sets up pieces as if user is 'WHITE'
        for i in range(0, 32):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2] + "_" + \
                                                                                   self.board_setup[i][3]

        self.click = 0
        self.validMoves = []

    # Enables grid and restart buttons when a character is chosen
    def pressWhite(self, event):
        self.User = EnableGame(self.White, self.Black, self.restart, self.chess, "WHITE")

        # Sets up the board with pieces
        for children in self.chess.GetChildren():
            PlacePiece("Chess/",
                       self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1],
                       children.GetWindow())

    def pressBlack(self, event):
        self.User = EnableGame(self.White, self.Black, self.restart, self.chess, "BLACK")

        # Sets up the board with pieces
        # Swaps White abd Black pieces
        for children in self.chess.GetChildren():
            PlacePiece("Chess/", self.Board[7 - (int(children.GetWindow().GetId() / 10) - 1)][
                7 - (children.GetWindow().GetId() % 10 - 1)], children.GetWindow())
        for children in self.chess.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][
                children.GetWindow().GetId() % 10 - 1] = children.GetWindow().GetName()

    def pressSolve(self, event):
        print("You are now in Solve Mode")

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        self.click = 0
        self.validMoves = []
        DisableGame(self.White, self.Black, self.restart, self.chess)
        for children in self.chess.GetChildren():
            self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
            PlacePiece("", "", children.GetWindow())
        for i in range(0, 32):
            self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2] + "_" + \
                                                                                   self.board_setup[i][3]

    # Places selected piece to where the user clicks next
    def btnChess(self, event):

        rowID = int(event.GetEventObject().GetId() / 10) - 1
        colID = event.GetEventObject().GetId() % 10 - 1

        # First click establishes which piece the user wants to move
        if self.click == 0:
            if event.GetEventObject().GetName()[:5] == self.User:
                self.click = event.GetEventObject().GetId()
                if event.GetEventObject().GetName()[6:] == "PAWN" and int(self.click/10)-1 == 6:
                    pMoved = False
                else:
                    pMoved = True
                self.validMoves = getValidChessMoves(int(self.click/10)-1,self.click%10-1,self.User,self.Board, pMoved)
                print(self.validMoves)

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if [rowID,colID] in self.validMoves:
                PlacePiece("Chess/", self.Board[int(self.click / 10) - 1][self.click % 10 - 1], event.GetEventObject())
                self.Board[rowID][colID] = self.Board[int(self.click / 10) - 1][self.click % 10 - 1]
                self.Board[int(self.click / 10) - 1][self.click % 10 - 1] = ""
                for children in self.chess.GetChildren():
                    if children.GetWindow().GetId() == self.click:
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
                self.validMoves = []
            else:
                self.click = event.GetEventObject().GetId()
                if event.GetEventObject().GetName()[6:] == "PAWN" and int(self.click/10)-1 == 6:
                    pMoved = False
                else:
                    pMoved = True
                self.validMoves = getValidChessMoves(int(self.click/10)-1,self.click%10-1,self.User,self.Board, pMoved)
                print(self.validMoves)

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.solve:
            self.StatusBar.SetStatusText("Calculate the best possible move")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# --------------------------------------------------------------------------------------------


# Runs Application
if __name__ == '__main__':
    app = wx.App()
    frame = Home()
    app.MainLoop()
