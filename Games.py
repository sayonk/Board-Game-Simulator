# Functions for all games

# wxpython used for GUI
import wx

# Used to extract game defaults from CSV files
import csv


# Enables the Game Grid  and restart button, and disables the character/colour buttons and returns the
# character/colour they chose

def EnableGame(C1, C2, RS, Grid, user):
    C1.Disable()
    C2.Disable()
    RS.SetLabel("Restart Game")
    for children in Grid.GetChildren():
        children.GetWindow().Enable()

    return user


# Disables the Games Grid and restart button, and enables the character/colour buttons
def DisableGame(C1, C2, RS, Grid):
    C1.Enable()
    C2.Enable()
    RS.SetLabel("Start Game")
    for children in Grid.GetChildren():
        children.GetWindow().Disable()


# Sets the button name and button bitmap accordingly when a piece is placed/moved
def PlacePiece(folder, text, window):
    if text == "button":
        pic = wx.Bitmap(1, 1)
        pic.SetMaskColour("black")
    else:
        pic = wx.Image(folder + text + ".png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    window.SetBitmap(pic)
    window.SetBitmapDisabled(pic)
    window.SetName(text)


# Extracts information from csv file and returns it as an array
def FromCSV(file):
    array = []
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array.append(row)
    except IOError:
        pass
    return array


# Sets up game grid
def gameGrid(game, panel, ROWS, COLS, COLOUR):

    # ROWSxCOLS Grid for the game
    game.grid = wx.GridSizer(ROWS, COLS, 0, 0)
    game.Board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            space = wx.Button(panel)
            game.grid.Add(space, 0, wx.EXPAND)
            row.append(space)
            space.Bind(wx.EVT_BUTTON, game.space)

            if COLOUR != "checkered":
                space.SetBackgroundColour(COLOUR)

            # Set ID to a value based on hash formula for easy access
            space.SetId((i + 10**int(ROWS/10)) * 10*(10**int(ROWS/10)) + (j + 10**int(COLS/10)))

        game.Board.append(row)

    # Colour board in a different way if the game is checkers or chess
    if COLOUR == "checkered":
        checkered(game.Board)

    return game


# Allows user to choose which mode to play in
def gameMode(game, panel):
    mode = wx.Choice(panel)
    mode.Append("One Player")
    mode.Append("Two Player")
    mode.Append("Solve")
    mode.SetSelection(0)
    mode.Bind(wx.EVT_ENTER_WINDOW, game.OnMouseEnter)
    mode.Bind(wx.EVT_LEAVE_WINDOW, game.OnMouseLeave)

    return mode


# Allows user to restart
def RS_Btn(game, panel):
    restart = wx.Button(panel, label='Start Game')
    restart.Bind(wx.EVT_BUTTON, game.pressRS)
    restart.Bind(wx.EVT_ENTER_WINDOW, game.OnMouseEnter)
    restart.Bind(wx.EVT_LEAVE_WINDOW, game.OnMouseLeave)

    return restart


# Sets up the layout of the games (Tic-Tac-Toe, Connect 4, Checkers, Chess)
def gameLayout(game, panel, ROWS, COLS, COLOUR, P1, P2):

    game = gameGrid(game, panel, ROWS, COLS, COLOUR)

    # Initialize user character
    game.User = ""

    # Allows user to choose which character to play as (O goes first, X goes second)
    game.player = wx.Choice(panel)
    game.player.Append(P1)
    game.player.Append(P2)
    game.player.SetSelection(0)
    game.player.Bind(wx.EVT_ENTER_WINDOW, game.OnMouseEnter)
    game.player.Bind(wx.EVT_LEAVE_WINDOW, game.OnMouseLeave)
    choose = wx.BoxSizer(wx.HORIZONTAL)
    choose.Add(game.player, 1, wx.ALL | wx.EXPAND, 5)

    game.mode = gameMode(game, panel)
    choose.Add(game.mode, 1, wx.ALL | wx.EXPAND, 5)

    game.restart = RS_Btn(game, panel)

    # Adds all buttons to the frame
    settings = wx.BoxSizer(wx.VERTICAL)
    settings.Add(game.grid, 1, wx.ALL | wx.EXPAND, 5)
    settings.Add(choose, 0, wx.ALL | wx.EXPAND, 5)
    settings.Add(game.restart, 0, wx.ALL | wx.EXPAND, 5)
    panel.SetSizer(settings)
    game.CreateStatusBar()
    game.Show()

    DisableGame(game.player, game.mode, game.restart, game.grid)

    return game


# Reset the game board when the Restart button is clicked
def resetGame(game):

    # Resets board to the setup before the character is chosen
    if game.restart.GetLabel() == "Restart Game":
        DisableGame(game.player, game.mode, game.restart, game.grid)

        # Remove all pieces from the board
        for children in game.grid.GetChildren():
            PlacePiece("", "button", children.GetWindow())

    # Enables grid and restart buttons when a character is chosen
    else:
        game.User = EnableGame(game.player, game.mode, game.restart, game.grid, game.player.GetStringSelection())
        print("You are now in " + game.mode.GetStringSelection() + " Mode")

        if game.gameName == "Checkers" or game.gameName == "Chess":

            # Sets up the board with pieces
            for rows in range(len(game.Board)):
                for cols in range(len(game.Board[rows])):
                    PlacePiece("assets/IMAGES/", game.Board[rows][cols].GetName(), game.Board[rows][cols])

        else:

            # Remove all pieces from the board
            for children in game.grid.GetChildren():
                PlacePiece("", "button", children.GetWindow())


# Describe buttons on hover
def onHover(game, e):
    if e.GetEventObject() == game.mode:
        game.StatusBar.SetStatusText("Choose a game mode")
    elif e.GetEventObject() == game.restart:
        game.StatusBar.SetStatusText("Start a new game")
    e.Skip()


# Remove description when not hovering
def offHover(game, e):
    game.StatusBar.SetStatusText("")
    e.Skip()


# Set up colours on a board in a checkered style
def checkered(board):

    for rows in range(len(board)):
        for cols in range(len(board[rows])):
            if (rows+cols) % 2:
                board[rows][cols].SetBackgroundColour("tan")
            else:
                board[rows][cols].SetBackgroundColour("wheat")

