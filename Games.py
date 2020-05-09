# Games Application
# Tic Tac Toe, Connect 4, Scrabble, Checkers, Chess

import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Board Games')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        TTT = wx.Button(panel, label='Tic-Tac-Toe')
        my_sizer.Add(TTT, 0, wx.ALL | wx.EXPAND, 5)
        
        C4 = wx.Button(panel, label='Connect Four')
        my_sizer.Add(C4, 0, wx.ALL | wx.EXPAND, 5)
        
        Scrab = wx.Button(panel, label='Scrabble')
        my_sizer.Add(Scrab, 0, wx.ALL | wx.EXPAND, 5)
        
        Check = wx.Button(panel, label='Checkers')
        my_sizer.Add(Check, 0, wx.ALL | wx.EXPAND, 5)
        
        Chess = wx.Button(panel, label='Chess')
        my_sizer.Add(Chess, 0, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(my_sizer)
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
    


