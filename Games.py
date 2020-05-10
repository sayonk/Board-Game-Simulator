# Games Application
# Tic Tac Toe, Connect 4, Scrabble, Checkers, Chess

# wxpython used for GUI
import wx

# Enables the Game Grid  and restart button, and disables the character/colour buttons
def EnableGame(C1,C2,RS,Grid):
    C1.Disable()
    C2.Disable()
    RS.Enable()
    for i in Grid.GetChildren():
        i.GetWindow().Enable()

# Disables the Games Grid and restart button, and enables the character/colour buttons
def DisableGame(C1,C2,RS,Grid):
    C1.Enable()
    C2.Enable()
    RS.Disable()
    for i in Grid.GetChildren():
        i.GetWindow().Disable()
    

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

        # 3x3 Grid for Tic-Tac-Toe
        self.ttt = wx.GridSizer(3, 3, 0, 0)
        for i in range(0,9):
            self.ttt.Add(wx.Button(panel),0,wx.EXPAND)

        # Allows user to choose which character to play as (O goes first, X goes second)
        self.O = wx.Button(panel, label='O')
        self.O.Bind(wx.EVT_BUTTON, self.pressO)
        self.X = wx.Button(panel, label='X')
        self.X.Bind(wx.EVT_BUTTON, self.pressX)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose O or X:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.O,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.X,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.ttt, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)
                   
        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.O,self.X,self.restart,self.ttt)

    # Enables grid and restart buttons when a character is chosen
    def pressO(self, event):
        EnableGame(self.O,self.X,self.restart,self.ttt) 

    def pressX(self, event):
        EnableGame(self.O,self.X,self.restart,self.ttt)

    def pressRS(self, event):
        DisableGame(self.O,self.X,self.restart,self.ttt)

class C4(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Connect Four')
        panel = wx.Panel(self)

        # 6x7 grid for Connect Four
        self.c4 = wx.GridSizer(6, 7, 0, 0)
        for i in range(0,42):
            self.c4.Add(wx.Button(panel),0,wx.EXPAND)

        # Allows user to choose which colour to play as (Red goes first, Yellow goes second)
        self.Red = wx.Button(panel, label='Red')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Yellow = wx.Button(panel, label='Yellow')
        self.Yellow.Bind(wx.EVT_BUTTON, self.pressYellow)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose Red or Yellow:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Yellow,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.c4, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.Red,self.Yellow,self.restart,self.c4)

    # Enables grid and restart buttons when a colour is chosen
    def pressRed(self, event):
        EnableGame(self.Red,self.Yellow,self.restart,self.c4) 

    def pressYellow(self, event):
        EnableGame(self.Red,self.Yellow,self.restart,self.c4)

    def pressRS(self, event):
        DisableGame(self.Red,self.Yellow,self.restart,self.c4)

class Scrab(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Scrabble')
        panel = wx.Panel(self)

        # 15x15 Grid for Scrabble
        scrab = wx.GridSizer(15, 15, 0, 0)
        for i in range(0,225):
            scrab.Add(wx.Button(panel),0,wx.EXPAND)

        # 7x1 Grid for Letter Rack
        rack = wx.GridSizer(1, 7, 0, 0)
        for i in range(0,7):
            rack.Add(wx.Button(panel),0,wx.EXPAND)

        # 2nd Row (Rack and Solve Mode)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(rack, 1, wx.ALL | wx.EXPAND, 5)
        row.Add(wx.Button(panel, label='Solve Mode'),0, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        restart = wx.Button(panel, label='Restart Game')

        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(scrab, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(row, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(restart, 0, wx.ALL | wx.EXPAND, 5)
  
        panel.SetSizer(settings)
        self.Show()

class Check(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Checkers')
        panel = wx.Panel(self)

        # 8x8 Grid for Checkers
        self.check = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            self.check.Add(wx.Button(panel),0,wx.EXPAND)

        # Allows user to choose which colour to play as (Red goes first, Black goes second)
        self.Red = wx.Button(panel, label='Red')
        self.Red.Bind(wx.EVT_BUTTON, self.pressRed)
        self.Black = wx.Button(panel, label='Black')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose Red or Black:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Red,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.check, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.Red,self.Black,self.restart,self.check)

    # Enables grid and restart buttons when a colour is chosen
    def pressRed(self, event):
        EnableGame(self.Red,self.Black,self.restart,self.check) 

    def pressBlack(self, event):
        EnableGame(self.Red,self.Black,self.restart,self.check)

    def pressRS(self, event):
        DisableGame(self.Red,self.Black,self.restart,self.check)

class Chess(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Chess')
        panel = wx.Panel(self)

        # 8x8 Grid for Chess
        self.chess = wx.GridSizer(8, 8, 0, 0)
        for i in range(0,64):
            self.chess.Add(wx.Button(panel),0,wx.EXPAND)

        # Allows user to choose which colour to play as (White goes first, Black goes second)
        self.White = wx.Button(panel, label='White')
        self.White.Bind(wx.EVT_BUTTON, self.pressWhite)
        self.Black = wx.Button(panel, label='Black')
        self.Black.Bind(wx.EVT_BUTTON, self.pressBlack)
        choose = wx.BoxSizer(wx.HORIZONTAL)
        choose.Add(wx.StaticText(panel, label='Choose White or Black:'),1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.White,1, wx.ALL | wx.EXPAND, 5)
        choose.Add(self.Black,1, wx.ALL | wx.EXPAND, 5)

        # Solve Mode
        choose.Add(wx.Button(panel, label='Solve Mode'),1, wx.ALL | wx.EXPAND, 5)

        # Allows user to restart
        self.restart = wx.Button(panel, label='Restart Game')
        self.restart.Bind(wx.EVT_BUTTON, self.pressRS)

        settings = wx.BoxSizer(wx.VERTICAL)
        settings.Add(self.chess, 1, wx.ALL | wx.EXPAND, 5)
        settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
        settings.Add(self.restart, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(settings)
        self.Show()

        DisableGame(self.White,self.Black,self.restart,self.chess)

    # Enables grid and restart buttons when a character is chosen
    def pressWhite(self, event):
        EnableGame(self.White,self.Black,self.restart,self.chess) 

    def pressBlack(self, event):
         EnableGame(self.White,self.Black,self.restart,self.chess)

    def pressRS(self, event):
        DisableGame(self.White,self.Black,self.restart,self.chess)
        

# Runs Application
if __name__ == '__main__':
    app = wx.App()
    frame = Home()
    app.MainLoop()
    
