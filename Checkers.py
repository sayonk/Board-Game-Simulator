# Checkers game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import DisableGame, FromCSV, EnableGame, PlacePiece


# Gets an array of valid checkers moves given the location of the piece chosen
def getValidCheckMoves(row, col, user, board):
    if user == "RED":
        opp = "BLACK"
    else:
        opp = "RED"

    arr = []

    # Checks whether the piece can go to a space diagonally
    for i in range(-1, 2):
        if i != 0:
            if row > 0 and 0 <= col + i <= 7 and board[row - 1][col + i] == "":
                arr.append([row - 1, col + i])
            elif row > 1 and 0 <= col + 2 * i <= 7 and board[row - 2][col + 2 * i] == "" and board[row - 1][col + i] \
                    == "":
                arr.append([row - 2, col + 2 * i])
    return arr


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
        self.player = wx.Choice(panel)
        self.player.Append("RED")
        self.player.Append("BLACK")
        self.player.SetSelection(0)
        self.player.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.player.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(self.player, 1, wx.ALL | wx.EXPAND, 5)

        # Allows user to choose which mode to play in
        self.mode = wx.Choice(panel)
        self.mode.Append("One Player")
        self.mode.Append("Two Player")
        self.mode.Append("Solve")
        self.mode.SetSelection(0)
        self.mode.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.mode.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        choose.Add(self.mode, 1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Start Game')
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

        DisableGame(self.player, self.mode, self.restart, self.check)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Checkers_Board.txt")

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

    def pressRS(self, event):
        self.click = 0
        self.validMoves = []

        # Resets board to the setup before the character is chosen
        if self.restart.GetLabel() == "Restart Game":
            DisableGame(self.player, self.mode, self.restart, self.check)
            for children in self.check.GetChildren():
                self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
                PlacePiece("", "", children.GetWindow())
            for i in range(0, 24):
                self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2]

        # Enables grid and restart buttons when a character is chosen
        else:
            p = self.player.GetStringSelection()
            self.User = EnableGame(self.player, self.mode, self.restart, self.check, p)
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

            # Sets up the board with pieces
            if p == "RED":
                for children in self.check.GetChildren():
                    PlacePiece("assets/IMAGES/",
                               self.Board[int(children.GetWindow().GetId() / 10) - 1][
                                   children.GetWindow().GetId() % 10 - 1],
                               children.GetWindow())

            # Sets up the board with pieces
            # Swaps Red and Black pieces
            else:
                for children in self.check.GetChildren():
                    PlacePiece("assets/IMAGES/", self.Board[7 - (int(children.GetWindow().GetId() / 10) - 1)][
                        7 - (children.GetWindow().GetId() % 10 - 1)], children.GetWindow())
                for children in self.check.GetChildren():
                    self.Board[int(children.GetWindow().GetId() / 10) - 1][
                        children.GetWindow().GetId() % 10 - 1] = children.GetWindow().GetName()

    # Moves selected piece to where the user clicks next
    def btnCheck(self, event):

        rowID = int(event.GetEventObject().GetId() / 10) - 1
        colID = event.GetEventObject().GetId() % 10 - 1

        # First click establishes which piece the user wants to move
        if self.click == 0:
            if event.GetEventObject().GetName() == self.User:
                self.click = event.GetEventObject().GetId()
                self.validMoves = getValidCheckMoves(rowID, colID, self.User, self.Board)

                # Highlight spaces where the selected piece can move to
                for children in self.check.GetChildren():
                    if [int(children.GetWindow().GetId() / 10) - 1, children.GetWindow().GetId() % 10 - 1] in \
                            self.validMoves:
                        children.GetWindow().SetBackgroundColour("green")

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if [rowID, colID] in self.validMoves:
                PlacePiece("assets/IMAGES/", self.Board[int(self.click / 10) - 1][self.click % 10 - 1],
                           event.GetEventObject())
                self.Board[int(event.GetEventObject().GetId() / 10) - 1][event.GetEventObject().GetId() % 10 - 1] = \
                    self.Board[int(self.click / 10) - 1][self.click % 10 - 1]
                self.Board[int(self.click / 10) - 1][self.click % 10 - 1] = ""
                for children in self.check.GetChildren():
                    if children.GetWindow().GetId() == self.click:
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
                self.validMoves = []

                # Colours board according to chess board layout
                i = 1
                switch = 0
                for children in self.check.GetChildren():
                    if i % 2 == switch:
                        children.GetWindow().SetBackgroundColour("tan")
                    else:
                        children.GetWindow().SetBackgroundColour("wheat")
                    if i % 8 == 0:
                        switch = 1 - switch
                    i += 1

            else:
                self.click = event.GetEventObject().GetId()
                self.validMoves = getValidCheckMoves(rowID, colID, self.User, self.Board)

                # Highlight spaces where the selected piece can move to
                i = 1
                switch = 0
                for children in self.check.GetChildren():
                    if [int(children.GetWindow().GetId() / 10) - 1, children.GetWindow().GetId() % 10 - 1] in \
                            self.validMoves and event.GetEventObject().GetName() == self.User:
                        children.GetWindow().SetBackgroundColour("green")
                    else:
                        if i % 2 == switch:
                            children.GetWindow().SetBackgroundColour("tan")
                        else:
                            children.GetWindow().SetBackgroundColour("wheat")
                    if i % 8 == 0:
                        switch = 1 - switch
                    i += 1

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.player:
            self.StatusBar.SetStatusText("Choose a player piece")
        elif event.GetEventObject() == self.mode:
            self.StatusBar.SetStatusText("Choose a game mode")
        elif event.GetEventObject() == self.restart:
            self.StatusBar.SetStatusText("Start a new game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()
