class Stats:
    def __init__(self, name, pruning):
        self.name = name

        self.pruning = pruning
        self.selectedPieces = []
        self.moveToLocations = []
        self.ourUtilitys = []
        self.times = []
        self.maxUtility = []
        self.board = []

    def addStats(self, selectedPiece, moveToLocation, ourUtility, time, maxUtility):
        self.selectedPieces.append(selectedPiece)
        self.moveToLocations.append(moveToLocation)
        self.ourUtilitys.append(ourUtility)
        self.times.append(time)
        self.maxUtility.append(maxUtility)

    def printStats(self, turn):
        print(f"Pruning: {self.pruning}")
        print(f"Turn: {turn * 2 + 1}")
        print(f"Time taken: {self.times[turn]}")
        print(f"utility score: {self.maxUtility[turn]}")
        print(f"selected piece: {self.selectedPieces[turn]}")
        print(f"move location: {self.moveToLocations[turn]}")
        print(f"max utility found: {self.ourUtilitys[turn]}")
        print()
        for i in range(8):
            for j in range(8):
                print("[", end='')
                if self.board[j][i] == -1:
                    print("X", end='')
                elif self.board[j][i] == 1:
                    print("O", end='')
                print("] ", end='')
            print()
        print()
        print()
