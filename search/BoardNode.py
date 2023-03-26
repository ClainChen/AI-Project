class BoardNode:
    def __init__(self, board: dict[tuple, tuple], parentNode, lastNode=None, nextNode=None):
        self.board = board
        self.level = 0
        self.heuristicScore = 0
        self.parentNode = parentNode
        self.lastNode = lastNode
        self.nextNode = nextNode
        self.changePosition = None
        self.changeDirection = None

    def win(self):
        """
        check current board is finished or not
        """
        for eachValue in self.board.values():
            if eachValue[0] == "b":
                return False
        return True

    def getParent(self):
        return self.parent

    def setLevel(self, level: int):
        self.level = level

    def getLevel(self):
        return self.level

    def setHeuristicScore(self, score: int):
        self.heuristicScore = score

    def getHeuristicScore(self):
        return self.heuristicScore

    def getBoard(self):
        return self.board

    def getIsRoot(self):
        return self.level == 0