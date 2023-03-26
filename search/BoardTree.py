class BoardTree:
    def __init__(self, board, parent=None):
        self.board = board
        self.level = 0
        self.heuristicScore = 0
        self.parent = parent
        self.up = None
        self.down = None
        self.rightUp = None
        self.rightDown = None
        self.leftUp = None
        self.leftDown = None

    def insertToDirection(self, direction: str, node):
        match direction:
            case "up":
                self.up = node
            case "down":
                self.down = node
            case "rightUp":
                self.rightUp = node
            case "rightDown":
                self.rightDown = node
            case "leftUp":
                self.leftUp = node
            case "leftDown":
                self.leftDown = node
            case _:
                print("The input direction is invalid!\n"
                      "Available direction: up, down, rightUp, rightDown, leftUp, leftDown")

    def getNodeAtDirection(self, direction: str):
        match direction:
            case "up":
                return self.up
            case "down":
                return self.down
            case "rightUp":
                return self.rightUp
            case "rightDown":
                return self.rightDown
            case "leftUp":
                return self.leftUp
            case "leftDown":
                return self.leftDown
            case _:
                print("The input direction is invalid!\n"
                      "Available direction: up, down, rightUp, rightDown, leftUp, leftDown")


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