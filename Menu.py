# Main menu

# wxpython used for GUI
import wx

# Imports frames from python files
from Checkers import Check
from Chess import Chess
from ConnectFour import C4
from Scrabble import Scrab
from TicTacToe import TTT


# Displays new frame for each game when button is clicked
def pressTTT(self):
    TTTFrame = TTT()
    TTTFrame.Show()


def pressC4(self):
    C4Frame = C4()
    C4Frame.Show()


def pressScrab(self):
    ScrabFrame = Scrab()
    ScrabFrame.Show()


def pressCheck(self):
    CheckFrame = Check()
    CheckFrame.Show()


def pressChess(self):
    ChessFrame = Chess()
    ChessFrame.Show()


# Creates Home Frame where user chooses which game to play
class Home(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Board Games', size=(300, 300))
        panel = wx.Panel(self)
        home = wx.BoxSizer(wx.VERTICAL)

        # Creates buttons for each game
        btnTTT = wx.Button(panel, label='Tic-Tac-Toe')
        btnTTT.Bind(wx.EVT_BUTTON, pressTTT)
        btnTTT.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnTTT.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnTTT, 0, wx.ALL | wx.EXPAND, 5)

        btnC4 = wx.Button(panel, label='Connect Four')
        btnC4.Bind(wx.EVT_BUTTON, pressC4)
        btnC4.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnC4.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnC4, 0, wx.ALL | wx.EXPAND, 5)

        btnScrab = wx.Button(panel, label='Scrabble')
        btnScrab.Bind(wx.EVT_BUTTON, pressScrab)
        btnScrab.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnScrab.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnScrab, 0, wx.ALL | wx.EXPAND, 5)

        btnCheck = wx.Button(panel, label='Checkers')
        btnCheck.Bind(wx.EVT_BUTTON, pressCheck)
        btnCheck.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnCheck.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnCheck, 0, wx.ALL | wx.EXPAND, 5)

        btnChess = wx.Button(panel, label='Chess')
        btnChess.Bind(wx.EVT_BUTTON, pressChess)
        btnChess.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        btnChess.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        home.Add(btnChess, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(home)
        self.CreateStatusBar()
        self.Show()

    def OnMouseEnter(self, event):
        self.StatusBar.SetStatusText("Click to open game")
        event.Skip()

    def OnMouseLeave(self, event):
        self.StatusBar.SetStatusText("")
        event.Skip()


# Runs Application
if __name__ == '__main__':
    app = wx.App()
    frame = Home()
    app.MainLoop()
