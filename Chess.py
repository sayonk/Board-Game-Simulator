# Chess game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import DisableGame, FromCSV, EnableGame, PlacePiece


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
        if row > 0 and board[row - 1][col] == "":
            arr.append([row - 1, col])
        for i in range(2):
            if row > 0 and 0 <= col + 1-2*i <= 7 and board[row - 1][col + 1-2*i][:5] == opp:
                arr.append([row - 1, col + 1-2*i])
        if not pMoved:
            arr.append([row - 2, col])

    # Checks each spot where the knight is an 'L shape' away from
    elif piece == "KNIGHT":
        for i in range(8):
            rowK = (-2 * (int(i / 2) % 2) + 1) * (i % 2 + 1)
            colK = ((i + 1) % 2 + 1) * (1 - 2 * int(i / 4))
            if 0 <= row + rowK <= 7 and 0 <= col + colK <= 7 and board[row + int(rowK)][col + int(colK)][:5] != user:
                arr.append([row + int(rowK), col + int(colK)])

    # Checks every spot where the piece can go based on their abilities
    else:
        if piece == "BISHOP" or piece == "ROOK":
            rng = 4
        else:
            rng = 8
        for i in range(rng):

            # Set formulas for each piece's abilities that can be calculated from the index number of the loop
            if piece == "BISHOP":
                rowP = -2 * (i % 2) + 1
                colP = -2 * int(i / 2) + 1
            elif piece == "ROOK":
                rowP = (i % 2) * (i - 2)
                colP = (1 - i % 2) * (i - 1)
            elif piece == "QUEEN" or piece == "KING":
                rowP = (-2 * (i % 2) + 1) * int(bool(i % 7))
                colP = int((i + 3) / 2) - 3 - int((int((i + 3) / 2) - 3) / 2)
            else:
                # If an empty space is chosen, there should be no valid spaces that are added to the list
                rowP = 8
                colP = 8

            # A piece cannot go any further if another piece is in the way
            blocked = False
            while not blocked:
                if 0 <= row + rowP <= 7 and 0 <= col + colP <= 7 and board[row + int(rowP)][col + int(colP)][
                                                                         :5] != user:
                    arr.append([row + int(rowP), col + int(colP)])
                    if board[row + int(rowP)][col + int(colP)][:5] == opp:
                        blocked = True
                else:
                    blocked = True
                if rowP != 0:
                    rowP += abs(rowP) / rowP
                if colP != 0:
                    colP += abs(colP) / colP
                if piece == "KING":
                    blocked = True
    return arr


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
        self.player = wx.Choice(panel)
        self.player.Append("WHITE")
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

        # Adds all buttons to frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.chess, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.player, self.mode, self.restart, self.chess)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Chess_Board.txt")

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

    # Resets board to the setup before the character is chosen
    def pressRS(self, event):
        self.click = 0
        self.validMoves = []

        # Resets board to the setup before the character is chosen
        if self.restart.GetLabel() == "Restart Game":
            DisableGame(self.player, self.mode, self.restart, self.chess)
            for children in self.chess.GetChildren():
                self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
                PlacePiece("", "", children.GetWindow())
            for i in range(0, 32):
                self.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] = self.board_setup[i][2] + "_" + \
                                                                                       self.board_setup[i][3]
        # Enables grid and restart buttons when a character is chosen
        else:
            p = self.player.GetStringSelection()
            self.User = EnableGame(self.player, self.mode, self.restart, self.chess, p)
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

            # Sets up the board with pieces
            if p == "WHITE":
                for children in self.chess.GetChildren():
                    PlacePiece("assets/IMAGES/",
                               self.Board[int(children.GetWindow().GetId() / 10) - 1][
                                   children.GetWindow().GetId() % 10 - 1],
                               children.GetWindow())

            # Sets up the board with pieces
            # Swaps White and Black pieces
            else:
                for children in self.chess.GetChildren():
                    PlacePiece("assets/IMAGES/", self.Board[7 - (int(children.GetWindow().GetId() / 10) - 1)][
                        7 - (children.GetWindow().GetId() % 10 - 1)], children.GetWindow())
                for children in self.chess.GetChildren():
                    self.Board[int(children.GetWindow().GetId() / 10) - 1][
                        children.GetWindow().GetId() % 10 - 1] = children.GetWindow().GetName()

    # Places selected piece to where the user clicks next
    def btnChess(self, event):

        rowID = int(event.GetEventObject().GetId() / 10) - 1
        colID = event.GetEventObject().GetId() % 10 - 1

        # First click establishes which piece the user wants to move
        if self.click == 0:
            if event.GetEventObject().GetName()[:5] == self.User:
                self.click = event.GetEventObject().GetId()
                if event.GetEventObject().GetName()[6:] == "PAWN" and int(self.click / 10) - 1 == 6:
                    pMoved = False
                else:
                    pMoved = True
                self.validMoves = getValidChessMoves(int(self.click / 10) - 1, self.click % 10 - 1, self.User,
                                                     self.Board, pMoved)

                # Highlight spaces where the selected piece can move to
                for children in self.chess.GetChildren():
                    if [int(children.GetWindow().GetId() / 10) - 1, children.GetWindow().GetId() % 10 - 1] in \
                            self.validMoves:
                        children.GetWindow().SetBackgroundColour("green")

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if [rowID, colID] in self.validMoves:
                PlacePiece("assets/IMAGES/", self.Board[int(self.click / 10) - 1][self.click % 10 - 1], event.GetEventObject())
                self.Board[rowID][colID] = self.Board[int(self.click / 10) - 1][self.click % 10 - 1]
                self.Board[int(self.click / 10) - 1][self.click % 10 - 1] = ""
                for children in self.chess.GetChildren():
                    if children.GetWindow().GetId() == self.click:
                        PlacePiece("", "", children.GetWindow())
                self.click = 0
                self.validMoves = []

                # Colours board according to chess board layout
                i = 1
                switch = 0
                for children in self.chess.GetChildren():
                    if i % 2 == switch:
                        children.GetWindow().SetBackgroundColour("tan")
                    else:
                        children.GetWindow().SetBackgroundColour("wheat")
                    if i % 8 == 0:
                        switch = 1 - switch
                    i += 1

            else:
                self.click = event.GetEventObject().GetId()
                if event.GetEventObject().GetName()[6:] == "PAWN" and int(self.click / 10) - 1 == 6:
                    pMoved = False
                else:
                    pMoved = True
                self.validMoves = getValidChessMoves(int(self.click / 10) - 1, self.click % 10 - 1, self.User,
                                                     self.Board, pMoved)

                # Highlight spaces where the selected piece can move to
                i = 1
                switch = 0
                for children in self.chess.GetChildren():
                    if [int(children.GetWindow().GetId() / 10) - 1, children.GetWindow().GetId() % 10 - 1] in \
                            self.validMoves and event.GetEventObject().GetName()[:5] == self.User:
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
