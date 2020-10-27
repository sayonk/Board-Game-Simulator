# Checkers game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import FromCSV, PlacePiece, gameLayout, resetGame, onHover, offHover, checkered


# Gets an array of valid checkers moves given the location of the piece chosen
def getValidCheckMoves(row, col, user, board):

    arr = []

    if user == "RED":
        opp = "BLACK"
    else:
        opp = "RED"

    # Checks whether the piece can go to a space diagonally
    if board[row][col].GetName() == user:
        for i in range(-1, 2):
            if i != 0:
                if row > 0 and 0 <= col + i <= 7 and board[row - 1][col + i].GetName() == "button":
                    arr.append([row - 1, col + i])
                elif row > 1 and 0 <= col + 2 * i <= 7 and board[row - 2][col + 2 * i].GetName() == "button" \
                        and board[row - 1][col + i].GetName() == "button":
                    arr.append([row - 2, col + 2 * i])

    return arr


# Highlights spaces on the board where the selected piece can move
def showMoves(self, event, rowID, colID):
    if event.GetEventObject().GetName() == self.game.User:
        self.click = event.GetEventObject().GetId()
        self.validMoves = getValidCheckMoves(rowID, colID, self.game.User, self.game.Board)

    if self.click > 0:
        checkered(self.game.Board)

    if event.GetEventObject().GetName() == self.game.User:
        # Highlight spaces where the selected piece can move to
        for moves in self.validMoves:
            self.game.Board[moves[0]][moves[1]].SetBackgroundColour("green")


class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers', size=(500, 550))
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 8, 8, "checkered", "Checkers", "RED", "BLACK")

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Checkers_Board.txt")

        self.click = 0
        self.validMoves = []

    def pressRS(self, event):

        self.click = 0
        self.validMoves = []

        # Resets board to the setup before the character is chosen
        if self.game.restart.GetLabel() == "Start Game":

            # Places pieces on the board based on which colour the user chooses
            for i in range(24):

                if self.game.player.GetStringSelection() == "RED":
                    self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])]\
                        .SetName(self.board_setup[i][2])
                else:
                    self.game.Board[7 - int(self.board_setup[i][0])][7 - int(self.board_setup[i][1])]\
                        .SetName(self.board_setup[i][2])

        # Reset the game board
        resetGame(self.game)
        checkered(self.game.Board)

    # Moves selected piece to where the user clicks next
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
