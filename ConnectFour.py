# Connect Four game

# wxpython used for GUI
import wx

# Import functions from main python file
from Games import DisableGame, EnableGame, PlacePiece


class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four', size=(500, 500))
        panel = wx.Panel(self)

        # 6x7 grid for Connect Four
        self.c4 = wx.GridSizer(6, 7, 0, 0)
        for i in range(0, 42):
            self.c4.Add(wx.Button(panel), 0, wx.EXPAND)
        for children in self.c4.GetChildren():
            children.GetWindow().Bind(wx.EVT_BUTTON, self.btnC4)
            children.GetWindow().SetBackgroundColour("medium blue")

        # Initialize user character
        self.User = ""

        # Allows user to choose which colour to play as (Red goes first, Yellow goes second)
        self.player = wx.Choice(panel)
        self.player.Append("RED")
        self.player.Append("YELLOW")
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
        settings.Add(self.c4, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(settings)
        self.CreateStatusBar()
        self.Show()

        DisableGame(self.player, self.mode, self.restart, self.c4)

        # Create 2D array for board
        self.Board = []

        # Populates array
        # The IDs of each button are set with a hash formula for easy access
        i = 0
        j = 0
        Brow = []
        for children in self.c4.GetChildren():
            children.GetWindow().SetId((i + 1) * 10 + (j + 1))
            Brow.append("")
            if j < 6:
                j += 1
            else:
                self.Board.append(Brow)
                Brow = []
                j = 0
                i += 1

    def pressRS(self, event):

        # Resets board to the setup before the character is chosen
        if self.restart.GetLabel() == "Restart Game":
            DisableGame(self.player, self.mode, self.restart, self.c4)
            for children in self.c4.GetChildren():
                self.Board[int(children.GetWindow().GetId() / 10) - 1][children.GetWindow().GetId() % 10 - 1] = ""
                PlacePiece("", "", children.GetWindow())

        # Enables grid and restart buttons when a character is chosen
        else:
            self.User = EnableGame(self.player, self.mode, self.restart, self.c4, self.player.GetStringSelection())
            print("You are now in " + self.mode.GetStringSelection() + " Mode")

    # Places piece in the lowest available spot in the selected column
    # The column is disabled when it becomes full
    def btnC4(self, event):
        col = event.GetEventObject().GetId() % 10 - 1
        for i in range(0, 6):
            if self.Board[i][col] == "" and (i == 5 or self.Board[i + 1][col] != ""):
                for children in self.c4.GetChildren():
                    if children.GetWindow().GetId() == (i + 1) * 10 + (col + 1):
                        PlacePiece("assets/IMAGES/", self.User, children.GetWindow())
                        self.Board[i][col] = self.User
                    if i == 0:
                        for disable in range(0, 6):
                            if children.GetWindow().GetId() == (disable + 1) * 10 + (col + 1):
                                children.GetWindow().Disable()

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
