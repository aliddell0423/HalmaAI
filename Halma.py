import math
from Stats import Stats
import time
from copy import deepcopy

GREEN = -1
BLANK = 0
RED = 1

class Halma(object):
    def __init__(self, size=8, load_board=None, timelimit=60):

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
        self.boards_generated = 0
        self.computerTime = 0
        self.timeLimit = timelimit
        self.currentTimer = time.time()
        self.pruning = True
        self.stats = Stats("stats", self.pruning)
        self.globalMoves = []
        self.searchDepth = 3
        self.maxUtility = float('-inf')
        self.chosenUtility = 0

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
            if self.board[poss_x][poss_y] == GREEN or \
                    self.board[poss_x][poss_y] == RED:
                if direction in filtered_poss_jumps:
                    jump_x = filtered_poss_jumps[direction][0]
                    jump_y = filtered_poss_jumps[direction][1]
                    if self.board[jump_x][jump_y] == BLANK:
                        if (jump_x, jump_y) not in self.movesList:
                            self.movesList.append((jump_x, jump_y))
                            self.findJumps(jump_x, jump_y, (x, y))




    def findAllMoves(self, x, y):
        movesList = []
        self.findJumps(x, y, None)
        movesList = self.movesList
        self.movesList = []
        poss_moves, poss_jumps = self.getPossMoves(x, y)
        filtered_moves = self.filterMoves(poss_moves)
        blanks = self.findBlanks(filtered_moves)

        for tup in blanks:
            movesList.append(tup)

        return movesList

    def switchTurns(self):
        temp = self.current
        self.current = self.opponent
        self.opponent = temp

    def checkForWin(self, board):

        is_win = True
        downcount = 4
        upcount = 0
        while downcount > 0:
            for i in range(downcount):
                if board[i][upcount] != RED:
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
                if board[-1-i][-1-upcount] != GREEN:
                    is_win = False
            downcount -= 1
            upcount += 1

        if is_win:
            return GREEN, True
        else:
            return None, False


    def manual_swap(self, board, start_x, start_y, goal_x, goal_y, color):

        def dist(x1, x2, y1, y2):
            return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

        board[goal_x][goal_y] = color
        board[start_x][start_y] = BLANK

        if goal_y > start_y and goal_x > start_x:
            return dist(start_x, goal_x, start_y, goal_y)*-10
        else:
            return dist(start_x, goal_x, start_y, goal_y) * 10


    # part 2 stuff

    def computerMove(self):

        self.boards_generated = 0
        t0 = time.time()
        eval, start, move = self.minimax2(self.board, GREEN, self.searchDepth, float('inf'), float('-inf'))
        self.manual_swap(self.board, start[0], start[1], move[0], move[1], GREEN)
        self.stats.addStats(start, move, eval, time.time() - t0, self.maxUtility)
        self.stats.board = self.board
        self.stats.printStats(int(self.turns / 2) - 1)
        self.maxUtility = float('-inf')



        #self.stats.printStats(self.turns - 1)


    # Utility function
    # given a board (2d array)
    # return some non-trivial measure of how strong that board is
    # the lower the number returned, the greater the utility (since its calculating distance to goal)
    def utility(self, board, color):
        # first, find the goal node that we will be comparing to
        # green in top left
        # red in bottom right

        temp_board = board
        if color == GREEN:
            # set the goal to be the bottom right
            goalNodeY = len(temp_board) - 1
            goalNodeX = len(temp_board) - 1
        else:  # color is red
            # set the goal to be the top left
            goalNodeY = 0
            goalNodeX = 0

        # loop through the board
        utilityValue = 0
        for row in range(self.size):
            for column in range(self.size):
                # see if the location is our color (a piece)
                # if it is, calculate the distance from our location to the preset goal
                distanceY = goalNodeY - row
                distanceX = goalNodeX - column
                if temp_board[row][column] == color:
                    # use the above for distance formuler calculation
                    utilityValue += math.sqrt((distanceY ** 2) + (distanceX ** 2))

        # at the end, return the utility value that we've calculated
        utilityValue = utilityValue * -1

        wincount = 0
        downcount = 4
        upcount = 0
        while downcount > 0:
            for i in range(downcount):
                if board[-1-i][-1-upcount] == GREEN:
                    wincount += 100
            downcount -= 1
            upcount += 1

        if utilityValue + wincount > self.maxUtility:
            self.maxUtility = utilityValue + wincount
        return utilityValue + wincount



    def minimax2(self, board, color, searchLimit, alpha, beta):

        maximizigPlayer = (color == GREEN)
        tempBoard = deepcopy(board)
        pieces = []
        start = (0, 0)
        goal_move = (0, 0)

        if searchLimit == 0 or self.checkForWin(tempBoard)[1]:
            self.boards_generated += 1
            return self.utility(tempBoard, GREEN)

        for i in range(self.size):
            for j in range(self.size):
                if tempBoard[i][j] == color:
                    pieces.append((i, j))

        if maximizigPlayer: # we will maximize by finding minimum
            maxEval = float('-inf')
            for piece in pieces:
                #print(f"piece: {piece}")
                move_list = self.findAllMoves(piece[0], piece[1])
                for move in move_list:
                    #print(f"move: {move}")
                    eval = self.manual_swap(tempBoard, piece[0], piece[1], move[0], move[1], GREEN)
                    eval += self.minimax2(tempBoard, RED, searchLimit - 1, alpha, beta)
                    self.manual_swap(tempBoard, move[0], move[1], piece[0], piece[1], GREEN)
                    #print(f"eval: {eval}")
                    if eval > maxEval:
                        maxEval = eval
                        start = piece
                        goal_move = move
                    if self.pruning:
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            if searchLimit == self.searchDepth:
                return maxEval, start, goal_move

            else:
                return maxEval
        else:
            minEval = float('inf')
            for piece in pieces:
                move_list = self.findAllMoves(piece[0], piece[1])
                for move in move_list:
                    eval = self.manual_swap(tempBoard, piece[0], piece[1], move[0], move[1], RED)
                    eval += self.minimax2(tempBoard, GREEN, searchLimit - 1, alpha, beta)
                    self.manual_swap(tempBoard, move[0], move[1], piece[0], piece[1], RED)
                    if eval < minEval:
                        minEval = eval
                    if self.pruning:
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return minEval




