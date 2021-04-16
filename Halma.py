GREEN_SELECTED = -2
GREEN = -1
BLANK = 0
RED = 1
RED_SELECTED = 2


class Halma(object):
    def __init__(self, size, load_board=None):

        self.size = size
        self.load_board = load_board
        if self.load_board == None:
            self.board = [[BLANK] * self.size for x in range(self.size)]
            downcount = 4
            upcount = 0
            while downcount > 0:
                for i in range(downcount):
                    self.board[i][upcount] = GREEN
                    self.board[-1-i][-1-upcount] = RED
                downcount -= 1
                upcount += 1
        else:
            self.board = load_board
        self.turns = 1  # Turn counter.
        self.current = RED  # Current player.
        self.opponent = GREEN
        self.player = RED
        self.computer = GREEN
        self.over = False
        self.movesList = []

    def __getitem__(self, i):
        return self.board[i]

    def getPossMoves(self, x, y):
        poss_moves = {
            "N": (x, y-1),
            "S": (x, y+1),
            "W": (x-1, y),
            "E": (x+1, y),
            "SW": (x-1, y+1),
            "SE": (x+1, y+1),
            "NW": (x-1, y-1),
            "NE": (x+1, y-1),
        }

        poss_jumps = {
            "N": (x, y-2),
            "S": (x, y+2),
            "W": (x-2, y),
            "E": (x+2, y),
            "SW": (x-2, y+2),
            "SE": (x+2, y+2),
            "NW": (x-2, y-2),
            "NE": (x+2, y-2),
        }

        return poss_moves, poss_jumps

    def filterMoves(self, moves_dict):
        filtered_dict = {}
        for direction, tup in moves_dict.items():
            if (0 <= tup[0] < self.size) and \
               (0 <= tup[1] < self.size):
                filtered_dict[direction] = tup
        return filtered_dict

    def findBlanks(self, filtered_dict):
        blanks = []

        for direction, tup in filtered_dict.items():
            x = tup[0]
            y = tup[1]

            if self.board[x][y] == BLANK:
                blanks.append(tup)

        return blanks

    def findJumps(self, x, y, prev_jump):
        poss_moves, poss_jumps = self.getPossMoves(x, y)
        filtered_poss_moves = self.filterMoves(poss_moves)
        filtered_poss_jumps = self.filterMoves(poss_jumps)

        for direction, tup in filtered_poss_moves.items():
            poss_x = tup[0]
            poss_y = tup[1]
            if self.board[poss_x][poss_y] == GREEN or self.board[poss_x][poss_y] == RED:
                if direction in filtered_poss_jumps:
                    jump_x = filtered_poss_jumps[direction][0]
                    jump_y = filtered_poss_jumps[direction][1]
                    if self.board[jump_x][jump_y] == BLANK:
                        if (jump_x, jump_y) not in self.movesList:
                            self.movesList.append((jump_x, jump_y))
                            self.findJumps(jump_x, jump_y, (x, y))



    def findAllMoves(self, x, y):
        self.findJumps(x, y, None)
        poss_moves, poss_jumps = self.getPossMoves(x, y)
        filtered_moves = self.filterMoves(poss_moves)
        blanks = self.findBlanks(filtered_moves)

        for tup in blanks:
            self.movesList.append(tup)

    def switchTurns(self):
        temp = self.current
        self.current = self.opponent
        self.opponent = temp

    def checkForWin(self):

        is_win = True
        downcount = 4
        upcount = 0
        while downcount > 0:
            for i in range(downcount):
                if self.board[i][upcount] != RED:
                    is_win = False
            downcount -= 1
            upcount += 1

        if is_win:
            return RED, True

        is_win = True
        downcount = 4
        upcount = 0
        while downcount > 0:
            for i in range(downcount):
                if self.board[-1-i][-1-upcount] != GREEN:
                    is_win = False
            downcount -= 1
            upcount += 1

        if is_win:
            return GREEN, True
        else:
            return None, False
