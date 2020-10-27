# Chess game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import FromCSV, PlacePiece, gameLayout, resetGame, onHover, offHover, checkered


# Gets an array of valid chess moves given the location of the piece chosen
def getValidChessMoves(row, col, user, board, pMoved):

    arr = []
    piece = board[row][col].GetName()[6:]

    if user == "WHITE":
        opp = "BLACK"
    else:
        opp = "WHITE"

    # If the pawn hasn't moved, it can move 2 up, otherwise only 1 up
    if piece == "PAWN":
        if row > 0 and board[row - 1][col].GetName() == "button":
            arr.append([row - 1, col])
        for i in range(2):
            if row > 0 and 0 <= col + 1-2*i <= 7 and board[row - 1][col + 1-2*i].GetName()[:5] == opp:
                arr.append([row - 1, col + 1-2*i])
        if not pMoved:
            arr.append([row - 2, col])

    # Checks each spot where the knight is an 'L shape' away from
    elif piece == "KNIGHT":
        for i in range(8):
            rowK = (-2 * (int(i / 2) % 2) + 1) * (i % 2 + 1)
            colK = ((i + 1) % 2 + 1) * (1 - 2 * int(i / 4))
            if 0 <= row + rowK <= 7 and 0 <= col + colK <= 7 and board[row + int(rowK)][col + int(colK)].GetName()[:5] \
                    != user:
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
                if 0 <= row + rowP <= 7 and 0 <= col + colP <= 7 and board[row + int(rowP)][col + int(colP)].GetName()[
                                                                         :5] != user:
                    arr.append([row + int(rowP), col + int(colP)])
                    if board[row + int(rowP)][col + int(colP)].GetName()[:5] == opp:
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


# Highlights spaces on the board where the selected piece can move
def showMoves(self, event, rowID, colID):
    if event.GetEventObject().GetName()[:5] == self.game.User:
        self.click = event.GetEventObject().GetId()
        if event.GetEventObject().GetName()[6:] == "PAWN" and int(self.click / 10) - 1 == 6:
            pMoved = False
        else:
            pMoved = True
        self.validMoves = getValidChessMoves(rowID, colID, self.game.User, self.game.Board, pMoved)
    if self.click > 0:
        checkered(self.game.Board)

    if event.GetEventObject().GetName()[:5] == self.game.User:
        # Highlight spaces where the selected piece can move to
        for moves in self.validMoves:
            self.game.Board[moves[0]][moves[1]].SetBackgroundColour("green")

    return self


class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess', size=(500, 550))
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 8, 8, "checkered", "Chess", "WHITE", "BLACK")

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Chess_Board.txt")

        self.click = 0
        self.validMoves = []

    def pressRS(self, event):

        self.click = 0
        self.validMoves = []

        # Resets board to the setup before the character is chosen
        if self.game.restart.GetLabel() == "Start Game":

            # Places pieces on the board based on which colour the user chooses
            for i in range(32):

                if self.game.player.GetStringSelection() == "WHITE":
                    self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])]\
                        .SetName(self.board_setup[i][2] + "_" + self.board_setup[i][3])
                else:
                    self.game.Board[7 - int(self.board_setup[i][0])][7 - int(self.board_setup[i][1])]\
                        .SetName(self.board_setup[i][2] + "_" + self.board_setup[i][3])

        # Reset the game board
        resetGame(self.game)
        checkered(self.game.Board)

    # Places selected piece to where the user clicks next
    def space(self, event):

        rowID = int(event.GetEventObject().GetId() / 10) - 1
        colID = event.GetEventObject().GetId() % 10 - 1

        # First click establishes which piece the user wants to move
        if self.click == 0:

            showMoves(self, event, rowID, colID)

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:
            if [rowID, colID] in self.validMoves:

                # Place piece in new space
                PlacePiece("assets/IMAGES/", self.game.Board[int(self.click / 10) - 1][self.click % 10 - 1].GetName(),
                           event.GetEventObject())

                # Remove piece from old space
                PlacePiece("", "button", self.game.Board[int(self.click / 10) - 1][self.click % 10 - 1])
                checkered(self.game.Board)

                self.click = 0
                self.validMoves = []

            else:

                showMoves(self, event, rowID, colID)

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
