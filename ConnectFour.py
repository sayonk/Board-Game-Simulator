# Connect Four game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import PlacePiece, getCol, userMoved, switchUser, gameLayout, resetGame, onHover, offHover


# Check and return the state of the game after each turn
def gameOver(self, row, col):
    over = "None"
    full = True

    temp_r = row - 1
    temp_c = col - 1

    horizontal = 1
    vertical = 1
    diagonal1 = 1
    diagonal2 = 1

    # Check horizontal line
    while horizontal < 4 and temp_c > -1 and self.game.Board[row][temp_c].GetName() \
            == self.game.Board[row][col].GetName():
        horizontal += 1
        temp_c -= 1
    temp_c = col + 1
    while horizontal < 4 and temp_c < 7 and self.game.Board[row][temp_c].GetName() == \
            self.game.Board[row][col].GetName():
        horizontal += 1
        temp_c += 1
    temp_c = col - 1

    # Check vertical line
    if horizontal < 4:
        while vertical < 4 and temp_r > -1 and self.game.Board[temp_r][col].GetName() == \
                self.game.Board[row][col].GetName():
            vertical += 1
            temp_r -= 1
        temp_r = row + 1
        while vertical < 4 and temp_r < 6 and self.game.Board[temp_r][col].GetName() == \
                self.game.Board[row][col].GetName():
            vertical += 1
            temp_r += 1
        temp_r = row - 1

        # Check first diagonal line
        if vertical < 4:
            while diagonal1 < 4 and temp_r > -1 and temp_c > -1 and self.game.Board[temp_r][temp_c].GetName() \
                    == self.game.Board[row][col].GetName():
                diagonal1 += 1
                temp_r -= 1
                temp_c -= 1
            temp_r = row + 1
            temp_c = col + 1
            while diagonal1 < 4 and temp_r < 6 and temp_c < 7 and self.game.Board[temp_r][temp_c].GetName() \
                    == self.game.Board[row][col].GetName():
                diagonal1 += 1
                temp_r += 1
                temp_c += 1
            temp_r = row - 1
            temp_c = col + 1

            # Check second diagonal line
            if diagonal1 < 4:
                while diagonal2 < 4 and temp_r > -1 and temp_c < 7 and self.game.Board[temp_r][temp_c].GetName() \
                        == self.game.Board[row][col].GetName():
                    diagonal2 += 1
                    temp_r -= 1
                    temp_c += 1
                temp_r = row + 1
                temp_c = col - 1
                while diagonal2 < 4 and temp_r < 6 and temp_c > -1 and self.game.Board[temp_r][temp_c].GetName() \
                        == self.game.Board[row][col].GetName():
                    diagonal2 += 1
                    temp_r += 1
                    temp_c -= 1
                if diagonal2 == 4:
                    over = self.game.User + " Wins!"
            else:
                over = self.game.User + " Wins!"
        else:
            over = self.game.User + " Wins!"
    else:
        over = self.game.User + " Wins!"

    # Check if there are any empty spots on the board
    for i in range(6):
        for j in range(7):
            if self.game.Board[i][j].GetName() == "button":
                full = False

    if over == "None" and full:
        over = "Tie Game!"

    switchUser(self)

    return over


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
        col = getCol(event.GetEventObject().GetId())
        row = 0
        for i in range(6):
            if self.game.Board[i][col].GetName() == "button" and (i == 5 or self.game.Board[i + 1][col].GetName() !=
                                                                  "button"):
                PlacePiece(self.game.User, self.game.Board[i][col], self.game.size)
                self.game.Board[i][col].SetName(self.game.User)

                if i == 0:
                    for disable in range(6):
                        self.game.Board[disable][col].Disable()

                row = i
                break

        userMoved(self, gameOver(self, row, col))

    def OnMouseEnter(self, event):
        if event.GetEventObject() == self.game.player:
            self.game.StatusBar.SetStatusText("Choose a player piece")
        onHover(self, event)

    def OnMouseLeave(self, event):
        offHover(self, event)
