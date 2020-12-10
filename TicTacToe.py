# Tic-Tac-Toe game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, getRow, getCol, userMoved, switchUser, gameLayout, resetGame, onHover, offHover


# Check and return the state of the game after each turn
def gameOver(self, event):
    over = "None"
    full = True

    row = getRow(event.GetEventObject().GetId())
    col = getCol(event.GetEventObject().GetId())

    # Check vertical and horizontal lines
    if self.game.Board[row][0].GetName() == self.game.Board[row][1].GetName() == self.game.Board[row][2].GetName() \
            or self.game.Board[0][col].GetName() == self.game.Board[1][col].GetName() \
            == self.game.Board[2][col].GetName():
        over = self.game.User + " Wins!"

    # Check diagonal lines
    if (abs(row - col) != 1) and (self.game.Board[0][0].GetName() == self.game.Board[1][1].GetName()
                                  == self.game.Board[2][2].GetName() != "button" or self.game.Board[0][2].GetName()
                                  == self.game.Board[1][1].GetName() == self.game.Board[2][0].GetName() != "button"):
        over = self.game.User + " Wins!"

    # Check if there are any empty spots on the board
    for i in range(3):
        for j in range(3):
            if self.game.Board[i][j].GetName() == "button":
                full = False

    if over == "None" and full:
        over = "Tie Game!"

    switchUser(self)

    return over


class TTT(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Tic Tac Toe', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 3, 3, "white", "TicTacToe", "CIRCLE", "CROSS", 60)

    def pressRS(self, event):
        # Reset the game board
        resetGame(self.game)

    # The button clicked is occupied by the User's character and is disabled
    def space(self, event):
        PlacePiece(self.game.User, event.GetEventObject(), self.game.size)
        event.GetEventObject().Disable()

        userMoved(self, gameOver(self, event))

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
