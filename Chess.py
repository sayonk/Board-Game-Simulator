# Chess game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, FromCSV, getRow, getCol, userMoved, switchUser, gameLayout, checkered, showMoves, \
    resetGame, onHover, offHover


# Check and return the state of the game after each turn
def gameOver(self):
    checkered(self.game, [self.king])

    switchUser(self)

    # Find the current user's king
    for i in range(8):
        for j in range(8):
            if self.game.Board[i][j].GetName()[:5] == self.game.User and self.game.Board[i][j].GetName()[6:] == "KING":
                self.king = [i, j]
                break

    # Set the king's space to red if it is in check
    if self.game.player.GetStringSelection() == self.game.User:
        opp = -1
    else:
        opp = 1

    if isCheck(self, opp, self.king, [], False):
        self.game.Board[self.king[0]][self.king[1]].SetBackgroundColour("red")

    # Check for 50 move draw
    if self.moves == 50:
        draw = True
    else:
        draw = False

    # Check for threefold repetition
    if not draw:
        position = positionToString(self)
        if position in self.board_positions:
            if position in self.board_positions2:
                draw = True
            else:
                self.board_positions2.append(position)
        else:
            self.board_positions.append(position)

    # Check for insufficient material
    if not draw:
        sameColourBishops = True
        for i in self.draw_scenarios:
            if sorted(self.pieces) == i:
                if len(i) == 4 and sameColourBishops:
                    first_bishop = ""
                    for j in range(8):
                        for k in range(8):
                            if self.game.Board[j][k].GetName()[6:] == "BISHOP":
                                if first_bishop == "":
                                    first_bishop = self.game.Board[j][k].GetBackgroundColour()
                                else:
                                    if self.game.Board[j][k].GetBackgroundColour() == first_bishop:
                                        draw = True
                                    else:
                                        sameColourBishops = False
                                    break
                else:
                    draw = True
                    break

    if not draw:
        getAllMoves(self)

    # Return the game result if the game is over
    if self.gameOver:
        if self.game.Board[self.king[0]][self.king[1]].GetBackgroundColour() == "red":
            return "Checkmate! " + self.game.Opp + " Wins!"
        else:
            return "Stalemate!"
    elif draw:
        return "Draw!"
    else:
        return "None"


# Convert the board position to a string
def positionToString(self):

    position = ""

    for i in range(8):
        for j in range(8):
            position += self.game.Board[i][j].GetName()

    return position


# Check if the king is in check given a possible move
def isCheck(self, opp, piece, spot, move):
    spot_piece = ""

    # Only move the piece if the boolean is true
    if move:
        spot_piece = self.game.Board[spot[0]][spot[1]].GetName()
        self.game.Board[spot[0]][spot[1]].SetName(self.game.Board[piece[0]][piece[1]].GetName())
        self.game.Board[piece[0]][piece[1]].SetName("button")

    check = False
    kingMoved = False

    if piece == self.king:

        if move:
            self.king = spot
            kingMoved = True

        if len(spot):
            check = pawnAndKnightMoves(self, "", spot[0], spot[1], opp, [], True)
        else:
            check = pawnAndKnightMoves(self, "", self.king[0], self.king[1], opp, [], True)

    if not check:
        for i in range(4):

            # Getting the coordinates for the diagonals from the king
            rowB = -2 * (i % 2) + 1
            colB = -2 * int(i / 2) + 1

            # Getting the coordinates for the files from the king
            rowR = (i % 2) * (i - 2)
            colR = (1 - i % 2) * (i - 1)

            if not move and len(spot):
                if self.game.Board[spot[0]][spot[1]].GetName() == "button":
                    check = getFullPath(self, opp, spot[0], spot[1], rowB, colB, "BISHOP", [], True)
                else:
                    check = True
            else:
                check = getFullPath(self, opp, self.king[0], self.king[1], rowB, colB, "BISHOP", [], True)
            if check:
                break

            if not move and len(spot):
                if self.game.Board[spot[0]][spot[1]].GetName() == "button":
                    check = getFullPath(self, opp, spot[0], spot[1], rowR, colR, "ROOK", [], True)
                else:
                    check = True
            else:
                check = getFullPath(self, opp, self.king[0], self.king[1], rowR, colR, "ROOK", [], True)
            if check:
                break

    # Undo the move
    if move:
        self.game.Board[piece[0]][piece[1]].SetName(self.game.Board[spot[0]][spot[1]].GetName())
        self.game.Board[spot[0]][spot[1]].SetName(spot_piece)

        if kingMoved:
            self.king = piece

    return check


# Add the move to the array if it is possible
def addMove(self, opp, piece, spot, move, arr):
    if not isCheck(self, opp, piece, spot, move):
        arr.append(spot)

    return arr


# Get the full path of a bishop, rook, queen, or king
def getFullPath(self, opp, row, col, rowP, colP, piece, arr, checking):
    check = False

    # A piece cannot go any further if another piece is in the way
    blocked = False
    while not blocked:
        if 0 <= row + rowP <= 7 and 0 <= col + colP <= 7 and \
                self.game.Board[row + int(rowP)][col + int(colP)].GetName()[:5] != self.game.User:

            if not checking:
                arr = addMove(self, opp, [row, col], [row + int(rowP), col + int(colP)], True, arr)

            if self.game.Board[row + int(rowP)][col + int(colP)].GetName()[:5] == self.game.Opp:
                blocked = True

                if checking and self.game.Board[row + int(rowP)][col + int(colP)].GetName()[6:] == piece or \
                        self.game.Board[row + int(rowP)][col + int(colP)].GetName()[6:] == "QUEEN" or \
                        (self.game.Board[row + int(rowP)][col + int(colP)].GetName()[6:] == "KING" and
                         -1 <= int(rowP) <= 1 and -1 <= int(colP) <= 1):
                    check = True

        else:
            blocked = True
        if rowP != 0:
            rowP += abs(rowP) / rowP
        if colP != 0:
            colP += abs(colP) / colP
        if not checking and piece == "KING":
            blocked = True

            # Check if castling is possible
            if self.game.Board[self.king[0]][self.king[1]].GetBackgroundColour() != "red":
                if opp == -1:
                    if self.UserK_castle and not isCheck(self, opp, self.king, [7, self.C_col[0]], False) and not \
                            isCheck(self, opp, self.king, [7, self.C_col[1]], False):
                        arr.append([7, self.C_col[2]])

                    if self.UserQ_castle and not isCheck(self, opp, self.king, [7, self.C_col[3]], False) and not \
                            isCheck(self, opp, self.king, [7, self.C_col[4]], False) and not \
                            isCheck(self, opp, self.king, [7, self.C_col[5]], False):
                        arr.append([7, self.C_col[4]])

                else:
                    if self.OppK_castle and not isCheck(self, opp, self.king, [0, self.C_col[0]], False) and not \
                            isCheck(self, opp, self.king, [0, self.C_col[1]], False):
                        arr.append([0, self.C_col[2]])

                    if self.OppQ_castle and not isCheck(self, opp, self.king, [0, self.C_col[3]], False) and not \
                            isCheck(self, opp, self.king, [0, self.C_col[4]], False) and not \
                            isCheck(self, opp, self.king, [0, self.C_col[5]], False):
                        arr.append([0, self.C_col[4]])

    if checking:
        return check
    else:
        return arr


# Get moves for the pawn and the knight
def pawnAndKnightMoves(self, piece, row, col, opp, arr, checking):
    check = False

    # If the pawn hasn't moved, it can move 2 up, otherwise only 1 up
    if piece == "PAWN" or checking:
        if not checking and 0 <= row + opp <= 7 and self.game.Board[row + opp][col].GetName() == "button":
            arr = addMove(self, opp, [row, col], [row + opp, col], True, arr)

        for i in range(2):
            if 0 <= col + 1 - 2 * i <= 7 and 0 <= row + opp <= 7 and \
                    self.game.Board[row + opp][col + 1 - 2 * i].GetName()[:5] == self.game.Opp:
                if checking:
                    if self.game.Board[row + opp][col + 1 - 2 * i].GetName()[6:] == "PAWN":
                        check = True

                else:
                    arr = addMove(self, opp, [row, col], [row + opp, col + 1 - 2 * i], True, arr)

        if not checking and row == opp + 7 * (1 - opp) / 2 and self.game.Board[row + opp][col].GetName() == "button" \
                and self.game.Board[row + 2 * opp][col].GetName() == "button":
            arr = addMove(self, opp, [row, col], [row + 2 * opp, col], True, arr)

        if not checking and len(self.poisson):
            for i in range(2):
                if 0 <= col + 1 - 2 * i <= 7 and [row, col + 1 - 2 * i] == self.poisson:
                    arr = addMove(self, opp, [row, col], [row + opp, col + 1 - 2 * i], True, arr)

    # Checks each spot where the knight is an 'L shape' away from
    if piece == "KNIGHT" or checking:
        for i in range(8):
            rowK = (-2 * (int(i / 2) % 2) + 1) * (i % 2 + 1)
            colK = ((i + 1) % 2 + 1) * (1 - 2 * int(i / 4))

            if 0 <= row + rowK <= 7 and 0 <= col + colK <= 7:
                if checking:
                    if self.game.Board[row + int(rowK)][col + int(colK)].GetName()[6:] == "KNIGHT" and \
                            self.game.Board[row + int(rowK)][col + int(colK)].GetName()[:5] == self.game.Opp:
                        check = True

                elif self.game.Board[row + int(rowK)][col + int(colK)].GetName()[:5] != self.game.User:
                    arr = addMove(self, opp, [row, col], [row + int(rowK), col + int(colK)], True, arr)

    if checking:
        return check
    else:
        return arr


# Gets an array of valid chess moves given the location of the piece chosen
def getValidChessMoves(self, row, col):
    arr = []
    piece = self.game.Board[row][col].GetName()[6:]

    if self.game.player.GetStringSelection() == self.game.User:
        opp = -1
    else:
        opp = 1

    if piece == "PAWN" or piece == "KNIGHT":

        arr = pawnAndKnightMoves(self, piece, row, col, opp, arr, False)

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

            arr = getFullPath(self, opp, row, col, rowP, colP, piece, arr, False)

    return arr


# Fill list of board spaces with lists of valid moves
def getAllMoves(self):
    self.gameOver = True

    for i in range(8):
        for j in range(8):

            if self.game.Board[i][j].GetName()[:5] == self.game.User:
                self.allMoves[i][j] = getValidChessMoves(self, i, j)

                if len(self.allMoves[i][j]):
                    self.gameOver = False
            else:
                self.allMoves[i][j] = []


class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess', size=(500, 550), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 8, 8, "checkered", "Chess", "WHITE", "BLACK", 50)

        # Extract info for chess board from csv file
        self.board_setup = FromCSV("assets/CSV/Chess_Board.txt")

        self.click = 0
        self.moves = 0
        self.allMoves = [[[] for i in range(8)] for j in range(8)]
        self.fSpots = []
        self.C_col = []
        self.poisson = []
        self.king = [0, 0]
        self.pieces = []
        self.board_positions = []
        self.board_positions2 = []
        self.gameOver = False
        self.UserK_castle = True
        self.UserQ_castle = True
        self.OppK_castle = True
        self.OppQ_castle = True

        self.draw_scenarios = [["BLACK_KING", "WHITE_KING"], ["BLACK_KING", "WHITE_BISHOP", "WHITE_KING"],
                               ["BLACK_BISHOP", "BLACK_KING", "WHITE_KING"],
                               ["BLACK_KING", "WHITE_KING", "WHITE_KNIGHT"],
                               ["BLACK_KING", "BLACK_KNIGHT", "WHITE_KING"],
                               ["BLACK_BISHOP", "BLACK_KING", "WHITE_BISHOP", "WHITE_KING"]]

    def pressRS(self, event):

        # Resets board to the setup before the character is chosen
        if self.game.restart.GetLabel() == "Start Game":

            self.pieces = []

            # Places pieces on the board based on which colour the user chooses
            for i in range(32):

                if self.game.player.GetStringSelection() == "WHITE":
                    self.game.Board[int(self.board_setup[i][0])][int(self.board_setup[i][1])] \
                        .SetName(self.board_setup[i][2] + "_" + self.board_setup[i][3])
                else:
                    self.game.Board[7 - int(self.board_setup[i][0])][7 - int(self.board_setup[i][1])] \
                        .SetName(self.board_setup[i][2] + "_" + self.board_setup[i][3])

                self.pieces.append(self.board_setup[i][2] + "_" + self.board_setup[i][3])

        # Reset the game board
        resetGame(self.game)
        if self.game.restart.GetLabel() == "Restart Game":

            if self.game.player.GetStringSelection() == "WHITE":
                self.king = [4, 7]
                self.C_col = [5, 6, 6, 1, 2, 3]
            else:
                self.king = [3, 0]
                self.C_col = [1, 2, 1, 4, 5, 6]
                switchUser(self.game)

            getAllMoves(self)

            self.click = 0
            self.moves = 0
            self.fSpots = []
            self.poisson = []
            self.board_positions = [positionToString(self)]
            self.board_positions2 = []
            self.UserK_castle = True
            self.UserQ_castle = True
            self.OppK_castle = True
            self.OppQ_castle = True

    # Places selected piece to where the user clicks next
    def space(self, event):

        rowID = getRow(event.GetEventObject().GetId())
        colID = getCol(event.GetEventObject().GetId())

        # First click establishes which piece the user wants to move
        if self.click == 0:

            if event.GetEventObject().GetName()[:5] == self.game.User:
                self.click = event.GetEventObject().GetId()

                showMoves(self.allMoves[rowID][colID], self.game.Board)

        # Second click moves the piece to the clicked spot
        # A new piece can be chosen to be moved by clicking on it
        else:

            self.moves += 0.5

            row_click = getRow(self.click)
            col_click = getCol(self.click)

            checkered(self.game, self.allMoves[row_click][col_click])

            if [rowID, colID] in self.allMoves[row_click][col_click]:

                pawnGraduate = False

                # Set castle boolean to False if one of the pieces are moved
                if self.game.Board[row_click][col_click].GetName()[6:] == "ROOK":
                    if col_click == 7:
                        if self.king[0] == 7:
                            if self.king[1] == 4:
                                self.UserK_castle = False
                            else:
                                self.UserQ_castle = False
                        else:
                            if self.king[1] == 4:
                                self.OppK_castle = False
                            else:
                                self.OppQ_castle = False
                    else:
                        if self.king[0] == 7:
                            if self.king[1] == 4:
                                self.UserQ_castle = False
                            else:
                                self.UserK_castle = False
                        else:
                            if self.king[1] == 4:
                                self.OppQ_castle = False
                            else:
                                self.OppK_castle = False

                # Move the rook if the king castles
                elif self.game.Board[row_click][col_click].GetName()[6:] == "KING":
                    if row_click == 7:
                        self.UserK_castle = False
                        self.UserQ_castle = False
                    else:
                        self.OppK_castle = False
                        self.OppQ_castle = False

                    if abs(self.king[1] - colID) == 2:
                        if colID == 6:
                            PlacePiece(self.game.Board[rowID][7].GetName(), self.game.Board[rowID][5], self.game.size)
                            PlacePiece("button", self.game.Board[rowID][7], self.game.size)
                        elif colID == 5:
                            PlacePiece(self.game.Board[rowID][7].GetName(), self.game.Board[rowID][4], self.game.size)
                            PlacePiece("button", self.game.Board[rowID][7], self.game.size)
                        elif colID == 2:
                            PlacePiece(self.game.Board[rowID][0].GetName(), self.game.Board[rowID][3], self.game.size)
                            PlacePiece("button", self.game.Board[rowID][0], self.game.size)
                        elif colID == 1:
                            PlacePiece(self.game.Board[rowID][0].GetName(), self.game.Board[rowID][2], self.game.size)
                            PlacePiece("button", self.game.Board[rowID][0], self.game.size)

                # Check for en poisson
                elif self.game.Board[row_click][col_click].GetName()[6:] == "PAWN":

                    self.moves = 0

                    if col_click != colID and event.GetEventObject().GetName() == "button":
                        self.pieces.remove(self.game.Board[self.poisson[0]][self.poisson[1]].GetName())
                        PlacePiece("button", self.game.Board[self.poisson[0]][self.poisson[1]], self.game.size)

                    elif abs(row_click - rowID) == 2:
                        self.poisson = [rowID, colID]
                    else:
                        self.poisson = []

                        if rowID == 0 or rowID == 7:
                            pawnGraduate = True

                # Remove taken piece from list of pieces
                if event.GetEventObject().GetName() != "button":
                    self.pieces.remove(event.GetEventObject().GetName())
                    self.moves = 0

                # Place piece in new space
                PlacePiece(self.game.Board[row_click][col_click].GetName(), event.GetEventObject(), self.game.size)

                # Remove piece from old space
                PlacePiece("button", self.game.Board[row_click][col_click], self.game.size)

                # Open a dialog to choose a piece when the pawn graduates
                if pawnGraduate:
                    dlg = wx.SingleChoiceDialog(self, "", "Choose a piece.",
                                                ["QUEEN", "ROOK", "BISHOP", "KNIGHT"], wx.OK)
                    if dlg.ShowModal() == wx.ID_OK:
                        PlacePiece(self.game.User + "_" + dlg.GetStringSelection(), event.GetEventObject(),
                                   self.game.size)
                        self.pieces.append(self.game.User + "_" + dlg.GetStringSelection())
                        self.pieces.remove(self.game.User + "_PAWN")
                    dlg.Destroy()

                self.click = 0
                userMoved(self, gameOver(self))

            else:

                if event.GetEventObject().GetName()[:5] == self.game.User:
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
