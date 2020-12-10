# Scrabble game

# Used to generate random integers
from random import randint

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, FromCSV, getRow, getCol, gameMode, RS_Btn, gameGrid, onHover, offHover


# Moves tiles from the rack or board to another spot on the rack or board
# Enables or Disables the play button if the play on the board is valid
def moveTile(self, event):

    # Condition if the user selected a piece from the rack
    if len(str(self.click)) == 1:

        previous_click = self.rack_arr[self.click]
        multiplier = ""

    # Condition if the user selected a piece from the board
    else:

        old_row = getRow(self.click)
        old_col = getCol(self.click)

        previous_click = self.game.Board[old_row][old_col]
        multiplier = self.multipliers[old_row][old_col]

        self.new_tiles.remove(self.click)

    event.GetEventObject().SetName(previous_click.GetName())

    # Open a dialog for the user to choose what they want to use the blank piece as

    if event.GetEventObject().GetName()[:5] == "BLANK":

        # Condition if the blank tile is selected from the rack
        if len(str(self.click)) == 1:

            # Only open dialog if it moves from the rack to the board
            if len(str(event.GetEventObject().GetId())) > 1:
                dlg = wx.TextEntryDialog(None, "Choose a letter")
                dlg.ShowModal()
                event.GetEventObject().SetName("BLANK_" + dlg.GetValue())
                dlg.Destroy()

        elif len(str(event.GetEventObject().GetId())) == 1:

            # Set the tile back to blank when it is returned to the rack
            event.GetEventObject().SetName("BLANK")

    # Condition that a space on the board was clicked
    if len(str(event.GetEventObject().GetId())) > 1:
        self.new_tiles.append(event.GetEventObject().GetId())

    # Condition that a space on the rack was clicked
    else:
        PlacePiece(event.GetEventObject().GetName(), event.GetEventObject(), self.size)

    self.click = -1

    # Remove tile from space that was clicked previously
    event.GetEventObject().SetLabel("")
    PlacePiece("button", previous_click, self.size)
    previous_click.SetLabel(multiplier)

    # Creates a temporary list to modify
    temp_list = list(self.new_tiles)
    words = []
    word_multipliers = []

    # Parses through placed tiles if there is at least one placed tile
    if len(self.new_tiles):

        # Only enable recall button when there are new tiles on the board
        self.Recall.Enable()

        tile = temp_list[0]
        row = getRow(tile)
        col = getCol(tile)

        # Sets direction of move if there are at least 2 new tiles
        direction = "HORIZONTAL"
        if len(temp_list) > 1 and getRow(temp_list[1]) != row:
            direction = "VERTICAL"

        touchCheck = False

        # Creates word by concatenating all connected tiles
        h_word = ""
        h_word_m = ""
        for i in range(2):
            while -1 < col < 15 and -1 < row < 15 and self.game.Board[row][col].GetName() != "button":

                # Starts from first tile and parses to the end, then goes back and parses to the start
                letter = self.game.Board[row][col]

                # Store multipliers in a string in the word_multiplier list
                if i:
                    # Make the letter lowercase to represent a blank tile used
                    if len(letter.GetName()) == 1:
                        h_word = letter.GetName()[-1] + h_word
                    else:
                        h_word = letter.GetName()[-1].lower() + h_word

                    if len(self.multipliers[row][col]) and letter.IsEnabled():
                        h_word_m = self.multipliers[row][col] + h_word_m
                    else:
                        h_word_m = "--" + h_word_m
                else:
                    if len(letter.GetName()) == 1:
                        h_word += letter.GetName()[-1]
                    else:
                        h_word += letter.GetName()[-1].lower()

                    if len(self.multipliers[row][col]) and letter.IsEnabled():
                        h_word_m += self.multipliers[row][col]
                    else:
                        h_word_m += "--"

                # Checks if at least one placed tile is touching a previously placed tile
                if self.game.Board[row][col].IsEnabled():

                    # Only check if this test has not already passed
                    if not touchCheck:

                        if row < 14 and not self.game.Board[row + 1][col].IsEnabled():
                            touchCheck = True
                        elif row > 0 and not self.game.Board[row - 1][col].IsEnabled():
                            touchCheck = True
                        elif col < 14 and not self.game.Board[row][col + 1].IsEnabled():
                            touchCheck = True
                        elif col > 0 and not self.game.Board[row][col - 1].IsEnabled():
                            touchCheck = True

                        # The centre piece must be filled on the first turn
                        elif self.game.Board[7][7].GetName() != "button" and self.game.Board[7][7].IsEnabled():
                            touchCheck = True

                    # Removes connected tiles so that duplicate parsing does not occur
                    temp_list.remove(self.game.Board[row][col].GetId())

                    # Checks the opposite direction for each newly placed tile
                    v_word = ""
                    v_word_m = ""
                    for j in range(2):
                        while -1 < col < 15 and -1 < row < 15 and self.game.Board[row][col].GetName() != "button":

                            letter = self.game.Board[row][col]

                            if j:
                                if len(letter.GetName()) == 1:
                                    v_word = letter.GetName()[-1] + v_word
                                else:
                                    v_word = letter.GetName()[-1].lower() + v_word

                                if len(self.multipliers[row][col]) and letter.IsEnabled():
                                    v_word_m = self.multipliers[row][col] + v_word_m
                                else:
                                    v_word_m = "--" + v_word_m
                            else:
                                if len(letter.GetName()) == 1:
                                    v_word += letter.GetName()[-1]
                                else:
                                    v_word += letter.GetName()[-1].lower()

                                if len(self.multipliers[row][col]) and letter.IsEnabled():
                                    v_word_m += self.multipliers[row][col]
                                else:
                                    v_word_m += "--"

                            if direction == "HORIZONTAL":
                                row += 1 - j * 2
                            else:
                                col += 1 - j * 2

                        if not j:
                            if direction == "HORIZONTAL":
                                row = getRow(tile) - 1
                            else:
                                col = getCol(tile) - 1

                    if len(v_word) > 1:
                        words.append(v_word)
                        word_multipliers.append(v_word_m)

                # Iterates whichever direction is currently being checked
                if direction == "HORIZONTAL":
                    col += 1 - i * 2
                    row = getRow(tile)
                else:
                    row += 1 - i * 2
                    col = getCol(tile)

            # Resets to the original tile and parse to the start
            if not i:
                if direction == "HORIZONTAL":
                    row = getRow(tile)
                    col = getCol(tile) - 1
                else:
                    row = getRow(tile) - 1
                    col = getCol(tile)

        # Add string to the list of words
        if len(h_word) > 1:
            words.append(h_word)
            word_multipliers.append(h_word_m)

        # Checks if each string in the list of words is a valid scrabble word
        wordCheck = True
        for word in words:
            if [word.lower()] not in self.dictionary:
                wordCheck = False

        # Checks if all tests are passed that qualifies the play as a valid play
        if touchCheck and wordCheck and not len(temp_list) and len(words):

            self.Play.Enable()
            for i in self.new_tiles:
                tile = self.game.Board[getRow(i)][getCol(i)]
                tile.SetBitmap(wx.Image("assets/IMAGES/GREEN_" + tile.GetName() + ".png", wx.BITMAP_TYPE_ANY)
                               .Scale(self.size, self.size).ConvertToBitmap())

            points = 0

            # Score the play based on the tiles and multipliers
            for i in range(len(words)):
                score = 0
                multiply = 1
                for j in range(len(words[i])):

                    if words[i][j].isupper():
                        letter_score = int(self.tiles_file[ord(words[i][j]) - 65][2])
                    else:
                        letter_score = 0
                    if word_multipliers[i][j * 2] != "-":
                        if word_multipliers[i][j * 2 + 1] == "L":
                            letter_score *= int(word_multipliers[i][j * 2])
                        else:
                            multiply *= int(word_multipliers[i][j * 2])
                    score += letter_score

                points += score * multiply

            if len(self.new_tiles) == 7:
                points += 50

            self.Points.SetLabel(str(points))
        else:
            self.Play.Disable()
            self.Points.SetLabel('0')
            for i in self.new_tiles:
                tile = self.game.Board[getRow(i)][getCol(i)]
                tile.SetBitmap(wx.Image("assets/IMAGES/RED_" + tile.GetName() + ".png", wx.BITMAP_TYPE_ANY)
                               .Scale(self.size, self.size).ConvertToBitmap())

    else:
        self.Play.Disable()
        self.Recall.Disable()
        self.Points.SetLabel('0')


# Takes tile from bag and places it on the rack
def takeTileFromBag(self, rack_spot):

    tile = randint(0, len(self.tiles) - 1)
    PlacePiece(self.tiles[tile], rack_spot, self.size)
    del self.tiles[tile]


# Resets the game board, racks, and tiles
def resetGame(self):
    self.new_tiles = []
    self.click = -1
    self.trade = False

    # Remove all tiles from the board
    for i in self.game.Board:
        for j in i:
            j.Disable()
            PlacePiece("button", j, self.size)

    # Fill board with multipliers
    for i in range(61):

        row = int(self.board_setup[i][0])
        col = int(self.board_setup[i][1])

        self.game.Board[row][col].SetLabel(self.multipliers[row][col])

        if self.multipliers[row][col] == "3W":
            self.game.Board[row][col].SetBackgroundColour("yellow")
        elif self.multipliers[row][col] == "2W":
            self.game.Board[row][col].SetBackgroundColour("red")
        elif self.multipliers[row][col] == "3L":
            self.game.Board[row][col].SetBackgroundColour("green")
        elif self.multipliers[row][col] == "2L":
            self.game.Board[row][col].SetBackgroundColour("blue")

    # Populate the bag with all tiles
    self.tiles = []
    for i in range(27):
        for j in range(int(self.tiles_file[i][1])):
            self.tiles.append(self.tiles_file[i][0])

    self.rack_arr = []
    self.comp_rack_arr = []

    # Who goes first is determined by chance
    value = randint(0, 1)
    for i in range(2):

        # Populates both racks with tiles from the bag randomly
        # Sets ID of rack buttons to its index number
        if i == value:
            j = 0
            for children in self.rack.GetChildren():
                tile = randint(0, len(self.tiles) - 1)
                PlacePiece(self.tiles[tile], children.GetWindow(), self.size)
                children.GetWindow().SetId(j)
                self.rack_arr.append(children.GetWindow())
                children.GetWindow().Disable()
                del self.tiles[tile]
                j += 1
        else:
            for j in range(7):
                tile = randint(0, len(self.tiles) - 1)
                self.comp_rack_arr.append(self.tiles[tile])
                del self.tiles[tile]

    self.Shuffle.Disable()
    self.Recall.Disable()
    self.Trade.Disable()
    self.Play.Disable()
    self.Points.SetLabel('0')
    self.PlayerScore.SetLabel('0')
    self.ComputerScore.SetLabel('0')


class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble', size=(600, 650),
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        self.size = 30

        # 7x1 Grid for Letter Rack
        self.rack = wx.GridSizer(1, 7, 0, 0)
        for i in range(7):
            self.rack.Add(wx.Button(panel), 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 3)
        for children in self.rack.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.pressrack)

        self.game = gameGrid(self, panel, 15, 15, "light blue", "Scrabble")
        self.mode = gameMode(self, panel)
        self.restart = RS_Btn(self, panel)

        # 2nd Row (Shuffle, Recall, Trade In, Score)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        self.Shuffle = wx.Button(panel, label='Shuffle')
        self.Shuffle.Bind(wx.EVT_BUTTON, self.pressShuffle)
        self.Shuffle.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Shuffle.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Recall = wx.Button(panel, label='Recall')
        self.Recall.Bind(wx.EVT_BUTTON, self.pressRecall)
        self.Recall.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Recall.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Trade = wx.Button(panel, label='Trade In')
        self.Trade.Bind(wx.EVT_BUTTON, self.pressTrade)
        self.Trade.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Trade.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Player = wx.StaticText(panel, label='Player: ')
        self.PlayerScore = wx.StaticText(panel, label='0')
        self.Computer = wx.StaticText(panel, label='Computer: ')
        self.ComputerScore = wx.StaticText(panel, label='0')

        row2.Add(self.Shuffle, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        row2.Add(self.Recall, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        row2.Add(self.Trade, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        row2.Add(self.Player, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 12)
        row2.Add(self.PlayerScore, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 12)
        row2.Add(self.Computer, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 12)
        row2.Add(self.ComputerScore, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 12)

        # 3rd Row (Rack, Current Score, Play, Mode)
        row3 = wx.BoxSizer(wx.HORIZONTAL)

        self.Play = wx.Button(panel, label='Play')
        self.Play.Bind(wx.EVT_BUTTON, self.pressPlay)
        self.Play.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Play.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Points = wx.StaticText(panel, label='0')
        self.Points.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Points.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

        row3.Add(self.rack, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        row3.Add(self.Points, 0, wx.ALL | wx.EXPAND, 10)
        row3.Add(self.Play, 0, wx.ALL | wx.EXPAND, 5)
        row3.Add(self.mode, 0, wx.ALL | wx.EXPAND, 5)

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.game.grid, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(row2, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(row3, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        # Extract info from scrabble files
        self.board_setup = FromCSV("assets/CSV/Scrabble_Board.txt")
        self.tiles_file = FromCSV("assets/CSV/Scrabble_Tiles.txt")
        self.dictionary = FromCSV("assets/CSV/Scrabble_Dictionary.txt")

        # Fill board with multipliers
        self.multipliers = [[""] * 15 for i in range(15)]
        for i in range(61):
            row = int(self.board_setup[i][0])
            col = int(self.board_setup[i][1])

            self.multipliers[row][col] = self.board_setup[i][2]

        # Initializes variables
        self.rack_arr = []
        self.comp_rack_arr = []
        self.tiles = []
        self.new_tiles = []
        self.trade_tiles = []
        self.click = -1
        self.trade = False

        resetGame(self)

    # Shuffles tiles in the rack
    def pressShuffle(self, event):

        self.click = -1

        for i in range(len(self.rack_arr)):
            if i < 6:
                value = randint(i, 6)
            else:
                value = 6

            temp = self.rack_arr[i].GetName()
            PlacePiece(self.rack_arr[value].GetName(), self.rack_arr[i], self.size)
            PlacePiece(temp, self.rack_arr[value], self.size)

    # Returns all tiles that were played in the current turn to the rack
    def pressRecall(self, event):

        self.click = -1

        if self.trade:

            for i in self.trade_tiles:
                i.SetBitmap(wx.Image("assets/IMAGES/" + i.GetName() + ".png", wx.BITMAP_TYPE_ANY)
                            .Scale(self.size, self.size).ConvertToBitmap())

            for children in self.game.grid.GetChildren():
                if children.GetWindow().GetName() == "button":
                    children.GetWindow().Enable()
            self.Shuffle.Enable()
            self.Trade.Enable()
            self.Recall.SetLabel('Recall')
            self.trade = False

        else:
            while len(self.new_tiles):

                # Removes tile from the board
                old_row = getRow(self.new_tiles[-1])
                old_col = getCol(self.new_tiles[-1])

                board_space = self.game.Board[old_row][old_col]
                multiplier = self.multipliers[old_row][old_col]

                del self.new_tiles[-1]

                # Iterates through rack until an empty space is found
                i = 0
                while self.rack_arr[i].GetName() != "button":
                    i += 1

                # Places tile from the board to the rack
                name = board_space.GetName()
                if name[:5] == "BLANK":
                    name = "BLANK"
                PlacePiece(name, self.rack_arr[i], self.size)
                PlacePiece("button", board_space, self.size)
                board_space.SetLabel(multiplier)

                self.click = -1

        self.Recall.Disable()

    # Trades tiles from the rack with tiles from the bag
    def pressTrade(self, event):

        self.click = -1

        # Returns tiles to the rack and disables the whole panel except for the rack
        if not self.trade:
            self.trade_tiles = []

            self.pressRecall(event)

            for children in self.game.grid.GetChildren():
                children.GetWindow().Disable()
            self.Shuffle.Disable()
            self.Play.Disable()
            self.Trade.Disable()
            self.Points.SetLabel('0')

            self.trade = True

            # Adds temporary cancel button in place of the recall button
            self.Recall.SetLabel('Cancel')
            self.Recall.Enable()

        else:

            tileNames = []

            for i in self.trade_tiles:
                tileNames.append(i.GetName())

                takeTileFromBag(self, i)

            for i in tileNames:
                self.tiles.append(i)

            for children in self.game.grid.GetChildren():
                if children.GetWindow().GetName() == "button":
                    children.GetWindow().Enable()
            self.Shuffle.Enable()
            self.Trade.Enable()
            self.trade = False

            self.Recall.SetLabel('Recall')
            self.Recall.Disable()

    # Disables tiles of the board when a word is played
    # Fills rest of rack with random remaining tiles
    def pressPlay(self, event):

        # Adds current score to total score
        self.PlayerScore.SetLabel(str(int(self.PlayerScore.GetLabel()) + int(self.Points.GetLabel())))
        self.Points.SetLabel('0')

        self.click = -1

        for tiles in self.new_tiles:
            tile = self.game.Board[getRow(tiles)][getCol(tiles)]
            tile.SetBackgroundColour("light blue")
            PlacePiece(tile.GetName(), tile, self.size)
            tile.Disable()

        self.new_tiles = []

        # Replaces empty spaces on the rack with new tiles from the bag
        for children in self.rack.GetChildren():
            if children.GetWindow().GetName() == "button" and len(self.tiles) > 0:

                takeTileFromBag(self, children.GetWindow())

        if len(self.tiles) < 7:
            self.Trade.Disable()

        # Disable Play button again after word has been played
        self.Play.Disable()
        self.Recall.Disable()

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):

        if self.restart.GetLabel() == "Restart Game":
            self.restart.SetLabel("Start Game")
            self.mode.Enable()

            resetGame(self)

        else:
            self.restart.SetLabel("Restart Game")
            self.mode.Disable()
            self.Shuffle.Enable()
            self.Trade.Enable()
            for children in self.rack:
                children.GetWindow().Enable()

            for children in self.game.grid:
                children.GetWindow().Enable()

    # Places the piece that was chosen onto an empty space on the board
    def space(self, event):

        # Selects the chosen pieces and places it where the user clicks next (back on rack or different place on board)
        if event.GetEventObject().GetName() != "button":

            self.click = event.GetEventObject().GetId()

        elif self.click > -1:

            moveTile(self, event)

    # Chooses a piece from the rack to place
    def pressrack(self, event):

        if not self.trade:
            if event.GetEventObject().GetName() != "button":

                self.click = event.GetEventObject().GetId()

            elif self.click > -1:

                moveTile(self, event)

        # Highlights border of tiles when clicked in trade in mode
        else:
            if event.GetEventObject().GetName() != "button":

                if event.GetEventObject() in self.trade_tiles:
                    event.GetEventObject().SetBitmap(wx.Image("assets/IMAGES/" + event.GetEventObject().GetName() +
                                                              ".png", wx.BITMAP_TYPE_ANY)
                                                     .Scale(self.size, self.size).ConvertToBitmap())
                    self.trade_tiles.remove(event.GetEventObject())
                else:
                    event.GetEventObject().SetBitmap(
                        wx.Image("assets/IMAGES/GREEN_" + event.GetEventObject().GetName() +
                                 ".png", wx.BITMAP_TYPE_ANY).Scale(self.size, self.size).ConvertToBitmap())
                    self.trade_tiles.append(event.GetEventObject())

                if len(self.trade_tiles):
                    self.Trade.Enable()
                else:
                    self.Trade.Disable()

    def OnMouseEnter(self, event):
        onHover(self, event)
        if event.GetEventObject() == self.Shuffle:
            self.StatusBar.SetStatusText("Shuffle the tiles in your rack")
        elif event.GetEventObject() == self.Play:
            self.StatusBar.SetStatusText("Play the new word onto the board")
        elif event.GetEventObject() == self.Recall:
            self.StatusBar.SetStatusText("Recall all the tiles you placed on the board this turn")
        elif event.GetEventObject() == self.Trade:
            self.StatusBar.SetStatusText("Skip your turn and trade in any number of tiles")
        event.Skip()

    def OnMouseLeave(self, event):
        offHover(self, event)
