# Connect Four game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, gameLayout, resetGame, onHover, offHover


class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four', size=(500, 500),
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        # Set up the game panel
        self.game = gameLayout(self, panel, 6, 7, "medium blue", "Connect4", "RED", "YELLOW", 40)

    def pressRS(self, event):

        # Reset the game board
        resetGame(self.game)

    # Places piece in the lowest available spot in the selected column
    # The column is disabled when it becomes full
    def space(self, event):
        col = event.GetEventObject().GetId() % 10 - 1
        for i in range(6):
            if self.game.Board[i][col].GetName() == "button" and (i == 5 or self.game.Board[i + 1][col].GetName() !=
                                                                  "button"):
                PlacePiece("assets/IMAGES/", self.game.User, self.game.Board[i][col], self.game.size)
                self.game.Board[i][col].SetName(self.game.User)

                if i == 0:
                    for disable in range(6):
                        self.game.Board[disable][col].Disable()

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
