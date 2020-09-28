# Scrabble game

# Used to generate random integers
from random import randint

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import FromCSV, onHover, offHover, gameMode, gameGrid, RS_Btn


# Resets the game board, racks, and tiles
def resetGame(self):
    # Populate the bag with all tiles
    for i in range(0, 27):
        for j in range(0, int(self.tiles_file[i][1])):
            self.tiles.append(self.tiles_file[i][0])

    # Fill board with multipliers
    self.multipliers = [[""] * 15 for i in range(15)]
    for i in range(0, 61):
        self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])].SetLabel(self.board_setup[i][2])
        self.multipliers[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]
        SetScrabColours(self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])])

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
                self.rack_arr.append(children.GetWindow())
                del self.tiles[tile]
                j += 1
        else:
            for j in range(0, 7):
                tile = randint(0, len(self.tiles) - 1)
                self.comp_rack_arr.append(self.tiles[tile])
                del self.tiles[tile]

    self.Shuffle.Disable()
    for children in self.rack:
        children.GetWindow().Disable()

    return self


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


# Moves tiles from the rack or board to another spot on the rack or board
def moveTile(self, event):
    # Condition if the user selected a piece from the rack
    if len(str(self.click)) == 1:
        event.GetEventObject().SetLabel(self.rack_arr[self.click].GetLabel())
        event.GetEventObject().SetBackgroundColour("tan")

        self.rack_arr[self.click].SetLabel("")
        self.rack_arr[self.click].SetBackgroundColour("grey")

    # Condition if the user selected a piece from the board
    else:
        old_row = int(self.click / 100) - 10
        old_col = self.click % 100 - 10

        event.GetEventObject().SetLabel(self.game.Board[old_row][old_col].GetLabel())
        event.GetEventObject().SetBackgroundColour("tan")

        self.game.Board[old_row][old_col].SetLabel(self.multipliers[old_row][old_col])
        SetScrabColours(self.game.Board[old_row][old_col])

    return self


# Enables or Disables the play button if the play on the board is valid
def checkValidity(self, event):

    # Updates the list of new tiles placed
    if len(str(event.GetEventObject().GetId())) > 1:
        self.new_tiles.append(event.GetEventObject().GetId())

        if len(str(self.click)) > 1:
            self.new_tiles.remove(self.click)

    else:
        self.new_tiles.remove(self.click)

    self.click = -1

    # Creates a temporary list to modify
    temp_list = list(self.new_tiles)
    words = []

    # Parses through placed tiles if there is at least one placed tile
    if len(self.new_tiles):
        tile = temp_list[0]
        row = int(tile / 100) - 10
        col = tile % 100 - 10

        # Sets direction of move if there are at least 2 new tiles
        direction = "HORIZONTAL"
        if len(temp_list) > 1 and int(temp_list[1] / 100) - 10 != row:
            direction = "VERTICAL"

        touchCheck = False

        # Creates word by concatenating all connected tiles
        h_word = ""
        for i in range(2):
            while len(self.game.Board[row][col].GetLabel()) == 1 and -1 < col < 15 and -1 < row < 15:

                # Starts from first tile and parses to the end, then goes back and parses to the start
                if i:
                    h_word = self.game.Board[row][col].GetLabel() + h_word
                else:
                    h_word += self.game.Board[row][col].GetLabel()

                # Checks if at least one placed tile is touching a previously placed tile
                if self.game.Board[row][col].IsEnabled():

                    if row < 14 and not self.game.Board[row + 1][col].IsEnabled():
                        touchCheck = True
                    elif row > 0 and not self.game.Board[row - 1][col].IsEnabled():
                        touchCheck = True
                    elif col < 14 and not self.game.Board[row][col + 1].IsEnabled():
                        touchCheck = True
                    elif col > 0 and not self.game.Board[row][col - 1].IsEnabled():
                        touchCheck = True

                    # The centre piece must be filled on the first turn
                    elif len(self.game.Board[7][7].GetLabel()) == 1 and self.game.Board[7][7].IsEnabled():
                        touchCheck = True

                    # Removes connected tiles so that duplicate parsing does not occur
                    temp_list.remove(self.game.Board[row][col].GetId())

                    # Checks the opposite direction for each newly placed tile
                    v_word = ""
                    for j in range(2):
                        while len(self.game.Board[row][col].GetLabel()) == 1 and -1 < col < 15 and -1 < row < 15:

                            if j:
                                v_word = self.game.Board[row][col].GetLabel() + v_word
                            else:
                                v_word += self.game.Board[row][col].GetLabel()

                            if direction == "HORIZONTAL":
                                row += 1 - j*2
                            else:
                                col += 1 - j*2

                        if not j:
                            if direction == "HORIZONTAL":
                                row = int(tile / 100) - 10 - 1
                            else:
                                col = tile % 100 - 10 - 1

                    if len(v_word) > 1:
                        words.append(v_word)

                # Iterates whichever direction is currently being checked
                if direction == "HORIZONTAL":
                    col += 1 - i*2
                    row = int(tile / 100) - 10
                else:
                    row += 1 - i*2
                    col = tile % 100 - 10

            # Resets to the original tile and parse to the start
            if not i:
                if direction == "HORIZONTAL":
                    row = int(tile / 100) - 10
                    col = tile % 100 - 10 - 1
                else:
                    row = int(tile / 100) - 10 - 1
                    col = tile % 100 - 10

        # Add string to the list of words
        if len(h_word) > 1:
            words.append(h_word)

        # Checks if each string in the list of words is a valid scrabble word
        wordCheck = True
        for word in words:
            if [word.lower()] not in self.dictionary:
                wordCheck = False

        # Checks if all tests are passed that qualifies the play as a valid play
        if touchCheck and wordCheck and not len(temp_list) and len(words):
            self.Play.Enable()
        else:
            self.Play.Disable()


class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble', size=(600, 650))
        panel = wx.Panel(self)

        # 7x1 Grid for Letter Rack
        self.rack = wx.GridSizer(1, 7, 0, 0)
        for i in range(0, 7):
            self.rack.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.rack.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressrack)
            children.GetWindow().SetBackgroundColour("tan")

        self.game = gameGrid(self, panel, 15, 15, "light blue")
        self.mode = gameMode(self, panel)
        self.restart = RS_Btn(self, panel)

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

        row.Add(self.rack, 1, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Shuffle, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Play, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.mode, 0, wx.ALL | wx.EXPAND, 5)

        # Disable Play button (Only gets enabled when a valid word is on the board)
        self.Play.Disable()

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.game.grid, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(row, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        # Extract info from scrabble files
        self.board_setup = FromCSV("assets/CSV/Scrabble_Board.txt")
        self.values = FromCSV("assets/CSV/Scrabble_Values.txt")
        self.tiles_file = FromCSV("assets/CSV/Scrabble_Tiles.txt")
        self.dictionary = FromCSV("assets/CSV/Scrabble_Dictionary.txt")

        # Initializes variables
        self.rack_arr = []
        self.comp_rack_arr = []
        self.tiles = []
        self.multipliers = []
        self.new_tiles = []
        self.click = -1

        resetGame(self)

    # Shuffles tiles in the rack
    def pressShuffle(self, event):
        self.click = -1
        for i in range(len(self.rack_arr)):
            value = randint(0, 7 - i - 1)

            temp = self.rack_arr[i].GetLabel()
            self.rack_arr[i].SetLabel(self.rack_arr[value].GetLabel())
            self.rack_arr[value].SetLabel(temp)

            if len(self.rack_arr[i].GetLabel()) == 1:
                self.rack_arr[i].SetBackgroundColour("tan")
            else:
                self.rack_arr[i].SetBackgroundColour("grey")

    # Disables tiles of the board when a word is played
    # Fills rest of rack with random remaining tiles
    def pressPlay(self, event):

        self.click = -1
        self.new_tiles = []

        for children in self.game.grid.GetChildren():
            if len(children.GetWindow().GetLabel()) == 1 and children.GetWindow().IsEnabled():
                children.GetWindow().Disable()

        for children in self.rack.GetChildren():
            if children.GetWindow().GetLabel() == "" and len(self.tiles) > 0:
                tile = randint(0, len(self.tiles) - 1)
                children.GetWindow().SetLabel(self.tiles[tile])
                children.GetWindow().SetBackgroundColour("tan")
                del self.tiles[tile]

        # Disable Play button again after word has been played
        self.Play.Disable()

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):

        if self.restart.GetLabel() == "Restart Game":
            self.restart.SetLabel("Start Game")
            self.mode.Enable()

            for rows in self.game.Board:
                for cols in rows:
                    cols.SetLabel("")

            resetGame(self)

        else:
            self.restart.SetLabel("Restart Game")
            self.mode.Disable()
            self.Shuffle.Enable()
            for children in self.rack:
                children.GetWindow().Enable()
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

    # Places the piece that was chosen onto an empty space on the board
    def space(self, event):

        # Selects the chosen pieces and places it where the user clicks next (back on rack or different place on board)
        if len(event.GetEventObject().GetLabel()) == 1:

            self.click = event.GetEventObject().GetId()

        elif self.click > -1:

            moveTile(self, event)
            checkValidity(self, event)

    # Chooses a piece from the rack to place
    def pressrack(self, event):
        if event.GetEventObject().GetLabel() != "":

            self.click = event.GetEventObject().GetId()

        elif self.click > -1:

            moveTile(self, event)
            checkValidity(self, event)

    def OnMouseEnter(self, event):
        onHover(self, event)
        if event.GetEventObject() == self.Shuffle:
            self.StatusBar.SetStatusText("Shuffle the tiles in your rack")
        elif event.GetEventObject() == self.Play:
            self.StatusBar.SetStatusText("Play the new word onto the board")
        event.Skip()

    def OnMouseLeave(self, event):
        offHover(self, event)
