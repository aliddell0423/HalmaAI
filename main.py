import wx
from Board import Frame

if __name__ == '__main__':
    app = wx.App(False)

    frame = Frame()
    frame.SetSize((1000, 1000))
    app.MainLoop()