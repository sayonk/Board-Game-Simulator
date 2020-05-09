# Games Application
# Tic Tac Toe, Connect 4, Scrabble, Checkers, Chess

# wxpython used for GUI
import wx

# Creates Home Frame where user chooses which game to play
class Home(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Board Games')
        panel = wx.Panel(self)
        home = wx.BoxSizer(wx.VERTICAL)

        # Creates buttons for each game
        TTT = wx.Button(panel, label='Tic-Tac-Toe')
        TTT.Bind(wx.EVT_BUTTON, self.pressTTT)
        home.Add(TTT, 0, wx.ALL | wx.EXPAND, 5)
        
        C4 = wx.Button(panel, label='Connect Four')
        C4.Bind(wx.EVT_BUTTON, self.pressC4)
        home.Add(C4, 0, wx.ALL | wx.EXPAND, 5)
        
        Scrab = wx.Button(panel, label='Scrabble')
        Scrab.Bind(wx.EVT_BUTTON, self.pressScrab)
        home.Add(Scrab, 0, wx.ALL | wx.EXPAND, 5)
        
        Check = wx.Button(panel, label='Checkers')
        Check.Bind(wx.EVT_BUTTON, self.pressCheck)
        home.Add(Check, 0, wx.ALL | wx.EXPAND, 5)
        
        Chess = wx.Button(panel, label='Chess')
        Chess.Bind(wx.EVT_BUTTON, self.pressChess)
        home.Add(Chess, 0, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(home)
        self.Show()

    # Displays new frame for each game when button is clicked
    def pressTTT(self, event):
        TTTFrame = TTT()
        TTTFrame.Show()

    def pressC4(self, event):
        C4Frame = C4()
        C4Frame.Show()

    def pressScrab(self, event):
        ScrabFrame = Scrab()
        ScrabFrame.Show()

    def pressCheck(self, event):
        CheckFrame = Check()
        CheckFrame.Show()

    def pressChess(self, event):
        ChessFrame = Chess()
        ChessFrame.Show()

# Creates frame for each game
class TTT(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Tic Tac Toe')
        panel = wx.Panel(self)
        ttt = wx.GridSizer(3, 3, 0, 0)
        for i in range(0,9):
            ttt.Add(wx.Button(panel),0,wx.EXPAND)
            
        panel.SetSizer(ttt)
        self.Show()

class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four')
        panel = wx.Panel(self)
        c4 = wx.GridSizer(6, 7, 0, 0)
        for i in range(0,42):
            c4.Add(wx.Button(panel),0,wx.EXPAND)
        panel.SetSizer(c4)
        self.Show()

class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble')
        panel = wx.Panel(self)
        scrab = wx.GridSizer(15, 15, 0, 0)
        for i in range(0,225):
            scrab.Add(wx.Button(panel),0,wx.EXPAND)        
        panel.SetSizer(scrab)
        self.Show()

class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers')
        panel = wx.Panel(self)
        check = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            check.Add(wx.Button(panel),0,wx.EXPAND)
        panel.SetSizer(check)
        self.Show()

class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess')
        panel = wx.Panel(self)
        chess = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            chess.Add(wx.Button(panel),0,wx.EXPAND) 
        panel.SetSizer(chess)
        self.Show()
        

# Runs Application
if __name__ == '__main__':
    app = wx.App()
    frame = Home()
    app.MainLoop()
    


