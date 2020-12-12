# Checkers game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, FromCSV, getRow, getCol, userMoved, switchUser, checkered, showMoves, gameLayout, \
    resetGame, onHover, offHover


# Check and return the state of the game after each turn
def gameOver(self):
    switchUser(self)
    getAllMoves(self)

    if self.UserP == 0 or self.OppP == 0:
        return self.game.Opp + " Wins!"
    else:
        for i in range(8):
            for j in range(8):
                if len(self.allMoves[i][j]):
                    return "None"
        return self.game.Opp + " Wins!"


# Gets the colour of the user based on the the piece name (king or not)
def getColour(piece):
    if len(piece.GetName()) > 6:
        return piece.GetName()[5:]
    else:
        return piece.GetName()


# Checks whether the piece can skip any of the opponents pieces
def skipOpp(self, row, col, opp):

    arr = []

    for i in range(-1, 2):
        if i != 0 and ((row > 1 and opp == -1) or (row < 6 and opp == 1)) and \
                (0 <= col + 2 * i <= 7 and self.game.Board[row + 2 * opp][col + 2 * i].GetName()
                 == "button" and getColour(self.game.Board[row + opp][col + i]) == self.game.Opp):

            self.oppSkipped[row][col].append((row + opp, col + i))
            arr.append((row + 2 * opp, col + 2 * i))

        if len(self.game.Board[row][col].GetName()) > 6 and i != 0 and \
                ((row < 6 and opp == -1) or (row > 1 and opp == 1)) and \
                (0 <= col + 2 * i <= 7 and self.game.Board[row - 2 * opp][col + 2 * i].GetName()
                 == "button" and getColour(self.game.Board[row - opp][col + i]) == self.game.Opp):

            self.oppSkipped[row][col].append((row - opp, col + i))
            arr.append((row - 2 * opp, col + 2 * i))

    return arr


# Gets an array of valid checkers moves given the location of the piece chosen
def getValidCheckMoves(self, row, col):

    if self.game.player.GetStringSelection() == self.game.User:
        opp = -1
    else:
        opp = 1

    arr = skipOpp(self, row, col, opp)

    # Checks whether the piece can go to a space diagonally only if there are no available skips
    if not len(arr):
        for i in range(-1, 2):
            if i != 0:
                if 0 <= col + i <= 7:
                    if 0 <= row + opp <= 7 and self.game.Board[row + opp][col + i].GetName() == "button":
                        arr.append((row + opp, col + i))
                        self.oppSkipped[row][col].append(())

                    if len(self.game.Board[row][col].GetName()) > 6 and 0 <= row - opp <= 7 and \
                            self.game.Board[row - opp][col + i].GetName() == "button":
                        arr.append((row - opp, col + i))
                        self.oppSkipped[row][col].append(())

    return arr


# Fill list of board spaces with lists of valid moves
def getAllMoves(self):
    for i in range(8):
        for j in range(8):
            self.oppSkipped[i][j] = []

            if getColour(self.game.Board[i][j]) == self.game.User:
                self.allMoves[i][j] = getValidCheckMoves(self, i, j)
            else:
                self.allMoves[i][j] = []


class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers', size=(500, 550),
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 8, 8, "checkered", "Checkers", "RED", "BLACK", 30)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Checkers_Board.txt")

        self.skip_again = False
        self.click = 0
        self.oppSkipped = [[[] for i in range(8)] for j in range(8)]
        self.allMoves = [[[] for i in range(8)] for j in range(8)]

        # Keep track of number of pieces per side
        self.UserP = 12
        self.OppP = 12

    def pressRS(self, event):

        # Resets board to the setup before the character is chosen
        if self.game.restart.GetLabel() == "Start Game":

            # Places pieces on the board based on which colour the user chooses
            for i in range(24):

                if self.game.player.GetStringSelection() == "RED":
                    self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] \
                        .SetName(self.board_setup[i][2])
                else:
                    self.game.Board[7 - int(self.board_setup[i][0])][7 - int(self.board_setup[i][1])] \
                        .SetName(self.board_setup[i][2])

        # Reset the game board
        resetGame(self.game)
        if self.game.restart.GetLabel() == "Restart Game":
            getAllMoves(self)

        self.skip_again = False
        self.click = 0

        self.UserP = 12
        self.OppP = 12

    # Moves selected piece to where the user clicks next
    def space(self, event):

        rowID = getRow(event.GetEventObject().GetId())
        colID = getCol(event.GetEventObject().GetId())

        # First click establishes which piece the user wants to move
        if self.click == 0:

            if getColour(event.GetEventObject()) == self.game.User:
                self.click = event.GetEventObject().GetId()

                showMoves(self.allMoves[rowID][colID], self.game.Board)

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:

            row_click = getRow(self.click)
            col_click = getCol(self.click)

            checkered(self.game, self.allMoves[row_click][col_click])

            moved = False

            for clicked_piece in range(len(self.allMoves[row_click][col_click])):

                if (rowID, colID) == self.allMoves[row_click][col_click][clicked_piece]:

                    moved = True

                    piece = self.game.Board[row_click][col_click]

                    # Set boolean to determine if a piece becomes a king in the current turn
                    kingMe = False

                    # Set piece to king if it reaches the end
                    if len(piece.GetName()) < 6 and (rowID == 0 or rowID == 7):
                        piece.SetName("KING_" + piece.GetName())

                        # Turn ends when a piece becomes a king
                        kingMe = True

                    # Place piece in new space
                    PlacePiece(piece.GetName(), event.GetEventObject(), self.game.size)

                    # Remove piece from old space
                    PlacePiece("button", piece, self.game.size)

                    # Remove skipped pieces
                    if len(self.oppSkipped[row_click][col_click][clicked_piece]):
                        PlacePiece("button", self.game.Board[self.oppSkipped[row_click][col_click][clicked_piece][0]][
                            self.oppSkipped[row_click][col_click][clicked_piece][1]], self.game.size)

                        if self.game.player.GetStringSelection() == self.game.User:
                            self.OppP -= 1
                            opp = -1
                        else:
                            self.UserP -= 1
                            opp = 1

                        # Disables all other clicks except mandatory extra skips when they are available
                        if not kingMe:
                            more_skips = skipOpp(self, rowID, colID, opp)
                            if len(more_skips):
                                self.skip_again = True
                                self.allMoves[rowID][colID] = more_skips
                                self.click = event.GetEventObject().GetId()
                                for skips in more_skips:
                                    self.game.Board[skips[0]][skips[1]].SetBackgroundColour("green")
                            else:
                                self.skip_again = False
                        else:
                            self.skip_again = False

                    if not self.skip_again:

                        self.click = 0
                        userMoved(self, gameOver(self))

                    break

            if not moved:

                if getColour(self.game.Board[rowID][colID]) == self.game.User:
                    checkered(self.game, self.allMoves[row_click][col_click])
                    showMoves(self.allMoves[rowID][colID], self.game.Board)
                    self.click = event.GetEventObject().GetId()
                else:
                    self.click = 0

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
