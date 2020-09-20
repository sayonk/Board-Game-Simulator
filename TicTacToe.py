# Tic-Tac-Toe game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import DisableGame, EnableGame, PlacePiece


class TTT(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Tic Tac Toe')
        panel = wx.Panel(self)

        # 3x3 Grid for Tic-Tac-Toe
        self.ttt = wx.GridSizer(3, 3, 0, 0)
        for i in range(0, 9):
            self.ttt.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.ttt.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnTTT)
            children.GetWindow().SetBackgroundColour("white")

        # Initialize user character
        self.User = ""

        # Allows user to choose which character to play as (O goes first, X goes second)
        self.player = wx.Choice(panel)
        self.player.Append("O")
        self.player.Append("X")
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

        # Adds all buttons to the frame
        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.ttt, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.player, self.mode, self.restart, self.ttt)

        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.ttt.GetChildren():
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 2:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    def pressRS(self, event):

        # Resets board to the setup before the character is chosen
        if self.restart.GetLabel() == "Restart Game":
            DisableGame(self.player, self.mode, self.restart, self.ttt)
            for children in self.ttt.GetChildren():
                self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
                PlacePiece("", "", children.GetWindow())

        # Enables grid and restart buttons when a character is chosen
        else:
            self.User = EnableGame(self.player, self.mode, self.restart, self.ttt, self.player.GetStringSelection())
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

    # The button clicked is occupied by the User's character and is disabled
    def btnTTT(self, event):
        self.Board[int(event.GetEventObject().GetId() / 10) - 1][event.GetEventObject().GetId() % 10 - 1] = self.User
        PlacePiece("assets/IMAGES/", self.User, event.GetEventObject())
        event.GetEventObject().Disable()

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
