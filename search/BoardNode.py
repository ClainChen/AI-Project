class BoardNode:
    def __init__(self, board: dict[tuple, tuple], parentNode, lastNode=None, nextNode=None):
        self.board = board
        self.level = 0
        self.cost = 0
        self.parentNode = parentNode
        self.lastNode = lastNode
        self.nextNode = nextNode
        self.changePosition = None
        self.changeDirection = None

    def win(self) -> bool:
        """
        check current board is finished or not
        """
        for eachValue in self.board.values():
            if eachValue[0] == "b":
                return False
        return True

    def getOutCome(self):
        return self.changePosition + self.changeDirection
