# Scrabble game

# Used to generate random integers
from random import randint

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import FromCSV


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

        # Allows user to choose which mode to play in
        self.mode = wx.Choice(panel)
        self.mode.Append("One Player")
        self.mode.Append("Two Player")
        self.mode.Append("Solve")
        self.mode.SetSelection(0)
        self.mode.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.mode.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        row.Add(self.rack, 1, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Shuffle, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.Play, 0, wx.ALL | wx.EXPAND, 5)
        row.Add(self.mode, 0, wx.ALL | wx.EXPAND, 5)

        # Disable Play button (Only gets enabled when a valid word is on the board)
        self.Play.Disable()

        # Allows user to restart
        self.restart = wx.Button(panel, label='Start Game')
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
        self.board_setup = FromCSV("assets/CSV/Scrabble_Board.txt")
        self.values = FromCSV("assets/CSV/Scrabble_Values.txt")
        self.tiles_file = FromCSV("assets/CSV/Scrabble_Tiles.txt")
        self.dictionary = FromCSV("assets/CSV/Scrabble_Dictionary.txt")

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

        if self.restart.GetLabel() == "Restart Game":
            self.restart.SetLabel("Start Game")
            self.mode.Enable()

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

        else:
            self.restart.SetLabel("Restart Game")
            self.mode.Disable()
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

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
        v_words = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        h_word = ""
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
                h_word += children.GetWindow().GetLabel()
                v_words[childColID] += children.GetWindow().GetLabel()
                if count_new > 0:
                    tiles_between += 1
                    rowIDs.append(childRowID)
                    colIDs.append(childColID)
                # Ends the word if the string goes until the end of the board
                if childColID == 14:
                    if len(h_word) > 1:
                        words.append(h_word)
                    h_word = ""
                if childRowID == 14:
                    if len(v_words[childColID]) > 1:
                        words.append(v_words[childColID])
                    v_words[childColID] = ""
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
                if len(h_word) > 1:
                    words.append(h_word)
                if len(v_words[childColID]) > 1:
                    words.append(v_words[childColID])
                h_word = ""
                v_words[childColID] = ""

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
                        while i < new_tiles[-1] + 1:
                            if rowIDs[i] == rowID:
                                if colIDs[i] != colID + j:
                                    check = False
                                j += 1
                            i += 1
                    else:
                        i = 1
                        j = 1
                        while i < new_tiles[-1] + 1:
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
        if event.GetEventObject() == self.mode:
            self.StatusBar.SetStatusText("Choose a game mode")
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
