# Tic-Tac-Toe game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, gameLayout, resetGame, onHover, offHover


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
        PlacePiece("assets/IMAGES/", self.game.User, event.GetEventObject(), self.game.size)
        event.GetEventObject().Disable()

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
