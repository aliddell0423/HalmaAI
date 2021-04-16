import wx
from Halma import Halma

GREEN_SELECTED = -2
GREEN = -1
BLANK = 0
RED = 1
RED_SELECTED = 2

class Frame(wx.Frame):
    def __init__(self, board=None, size=None):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None, -1, "Halma", style=style)


        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.selectStone)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.moveStone)
        self.panel.Bind(wx.EVT_PAINT, self.Refresh)

        self.size = 0

        self.Newgame(None, board, size)

        menu = wx.Menu()
        menu.Append(1, "New Game")
        menu.AppendSeparator()
        menu.Append(2, "Load Board")
        menu.AppendSeparator()
        menu.Append(3, "Save Board")
        menu.AppendSeparator()
        menu.Append(4, "Quit")

        menubar = wx.MenuBar()
        menubar.Append(menu, "Menu")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.Newgame, id=1)
        self.Bind(wx.EVT_MENU, self.Loadgame, id=2)
        self.Bind(wx.EVT_MENU, self.Savegame, id=3)
        self.Bind(wx.EVT_MENU, self.Quit, id=4)

        self.CreateStatusBar()

        self.selected = (-1, -1)

        self.Show()


    def Quit(self, event):
        self.Close()

    def Newgame(self, event, board=None, size=None):
        if size == None:
            size = self.chooseSize()
        self.size = size
        self.halma = Halma(size, board)
        self.panel.Refresh()

    def Loadgame(self, event):
        i = []
        j = []
        size = 0
        dlg = wx.FileDialog(parent=None,
                            message='Load board file',
                            defaultDir="",
                            defaultFile="")
        dlg.ShowModal()
        filename = dlg.GetFilename()
        f = open(filename, "r")
        for line in f:
            size += 1
            num_list = line.split(' ')
            for num in num_list:
                if num != '\n':
                    j.append(int(num))
            i.append(j)
            j = []

        self.Newgame(event=None, board=i, size=size)




    def Savegame(self, event):
        dlg = wx.TextEntryDialog(parent=None,
                                 message='Name your file')
        dlg.ShowModal()
        filename = dlg.GetValue()
        f = open(filename, "w")
        for i in range(self.size):
            for j in range(self.size):
                f.write(str(self.halma.board[i][j]))
                f.write(" ")
            f.write("\n")
        f.close()

    def chooseSize(self):
        sizes = ["8", "10", "16"]
        dlg = wx.SingleChoiceDialog(parent=None,
                                    message='Choose a board size:',
                                    caption='New Game',
                                    choices=sizes,
                                    pos=wx.DefaultPosition)
        dlg.ShowModal()
        choice = int(dlg.GetStringSelection())
        self.size = choice
        return choice


    def selectStone(self, event):
        self.halma.movesList = []
        x, y = self.getClickLoc(event)

        prev_x = self.selected[0]
        prev_y = self.selected[1]

        if self.halma.board[x][y] == self.halma.current:
            self.halma.findAllMoves(x, y)

        if self.halma.board[x][y] == self.halma.current:
            if self.halma.board[prev_x][prev_y] == GREEN_SELECTED:
                self.halma.board[prev_x][prev_y] = GREEN
            elif self.halma.board[prev_x][prev_y] == RED_SELECTED:
                self.halma.board[prev_x][prev_y] = RED
            if self.halma.current == RED:
                self.halma.board[x][y] = RED_SELECTED
            else:
                self.halma.board[x][y] = GREEN_SELECTED

            self.selected = (x, y)

        self.panel.Refresh()

    def moveStone(self, event):
        x, y = self.getClickLoc(event)

        if (x, y) not in self.halma.movesList:
            event.Skip()
        else:
            self.swap(x, y)
            self.selected = (-1, -1)
            self.halma.movesList = []
            self.halma.turns += 1
            self.halma.switchTurns()
            color, is_win = self.halma.checkForWin()
            if is_win:
                self.displayWinner(color)
            self.panel.Refresh()

    def displayWinner(self, color):
        print(color)
        if color == self.halma.player:
            winner = "player"
        else:
            winner = "computer"

        self.Notify("Game Over!", f"The {winner} has won!")

    def Notify(self, caption, message):
        dialog = wx.MessageDialog(None,
                                  message=message,
                                  caption=caption,
                                  style=wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def swap(self, x, y):
        self.halma.board[x][y] = self.halma.current
        start_x = self.selected[0]
        start_y = self.selected[1]

        self.halma.board[start_x][start_y] = BLANK

    def getClickLoc(self, event):
        winx, winy = event.GetX(), event.GetY()
        w, h = self.panel.GetSize()
        x = winx / (w / self.halma.size)
        y = winy / (h / self.halma.size)

        x = int(x)
        y = int(y)

        return x, y


    def Refresh(self, event):
        dc = wx.AutoBufferedPaintDCFactory(self.panel)
        dc = wx.GCDC(dc)
        self.SetStatusText("Current player is " + ["Green", "Red"][self.halma.current == RED])
        w, h = self.panel.GetSize()

        dc.SetBrush(wx.Brush("white"))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetBrush(wx.Brush("gray"))
        px, py = w / self.size, h / self.size

        color = "gray"
        for i in range(self.size):
            if color == "gray":
                color = "white"
            else:
                color = "gray"
            for j in range(self.size):
                if color == "gray":
                    color = "white"
                else:
                    color = "gray"
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(j*px, i*py, px, py)

        brushes = {GREEN: wx.Brush("green"),
                   RED: wx.Brush("red"),
                   RED_SELECTED: wx.Brush("pink"),
                   GREEN_SELECTED: wx.Brush("#58ffdf") }
        for i in range(self.size):
            for j in range(self.size):
                c = self.halma[i][j]
                if c != BLANK:
                    dc.SetBrush(brushes[c])
                    dc.DrawEllipse(i * px, j * py, px, py)
                elif c == RED_SELECTED or c == GREEN_SELECTED:
                    dc.SetBrush("orange")
                    dc.DrawRectangle(j * px, i * py, px, py)
                elif (i, j) in self.halma.movesList:
                    dc.SetBrush(wx.Brush("red"))
                    dc.DrawCircle(i * px + px / 2, j * py + py / 2, 3)
