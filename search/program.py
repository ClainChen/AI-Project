# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board
from BoardNode import BoardNode

"""
The Dictionary which stores the move method
Key is the string which describe the direction of movement
Value is the coordinate translation which store with tuple
"""
moveDirection: dict[str, tuple[int, int]] = {
    "up": (1, -1),
    "down": (-1, 1),
    "rightUp": (1, 0),
    "rightDown": (0, 1),
    "leftUp": (0, -1),
    "leftDown": (-1, 0)
}


def movement(currentPosition: tuple, direction: tuple) -> tuple[int, int]:
    """
    This method is use for generate the new position with currentPosition and move direction
    """
    x = currentPosition[0] + direction[0]
    y = currentPosition[1] + direction[1]
    if x > 6:
        x = 0
    if x < 0:
        x = 6
    if y > 6:
        y = 0
    if y < 0:
        y = 6
    newPosition = (x, y)
    return newPosition


def addition(value: int) -> int:
    return 0 if value + 1 > 6 else value + 1


def spread(chessBoard: dict[tuple, tuple], position: tuple) -> list[dict[tuple, tuple]]:
    """
    This method is use for spread a red chess to the specific direction
    This Return a new Board after finish spread
    """
    """
    两个异常处理在一定情况下并没有什么用，但是可以用来测试bug
    后期可以直接删掉
    """
    try:
        operatingChess = chessBoard[position]
    except KeyError:
        print("This position do not have any chess!")
        return []
    else:
        if operatingChess[0] != "r":
            print("The red chess is not in this cell!")
            return []

        else:
            result = []
            chessLevel = operatingChess[1]
            for key in moveDirection.keys():
                interPos = position
                # print("moving", key)
                direction = moveDirection[key]
                interBoard = chessBoard.copy()
                for i in range(chessLevel):
                    newPos = movement(interPos, direction)
                    # print("New Position: ", newPos)
                    if interBoard.__contains__(newPos):
                        value = interBoard[newPos][1]
                        newTuple = ("r", addition(value))
                        interBoard[newPos] = newTuple
                    else:
                        interBoard[newPos] = ("r", 1)
                    interPos = newPos
                # Delete the original cell in position
                del interBoard[position]
                result.append(interBoard)
                # print("----------")

            return result


def single_spread(chessBoard: dict[tuple, tuple], position: tuple, direction: str) -> dict[tuple, tuple]:
    """
    Spread a chess to a specific direction
    """
    if direction not in moveDirection.keys():
        print("This direction is invalid")
        return {}

    try:
        operatingChess = chessBoard[position]
    except KeyError:
        print("This position do not have any chess!")
        return {}
    else:
        if operatingChess[0] != "r":
            print("The red chess is not in this cell!")
            return {}

        else:
            chessLevel = operatingChess[1]
            interPos = position
            # print("moving", key)
            interBoard = chessBoard.copy()
            direction = moveDirection[direction]
            for i in range(chessLevel):
                newPos = movement(interPos, direction)
                # print("New Position: ", newPos)
                if interBoard.__contains__(newPos):
                    value = interBoard[newPos][1]
                    newTuple = ("r", addition(value))
                    interBoard[newPos] = newTuple
                else:
                    interBoard[newPos] = ("r", 1)
                interPos = newPos
            # Delete the original cell in position
            del interBoard[position]
            result = interBoard
            # print("----------")
            return result


def heuristic(chessBoard: dict[tuple, tuple]) -> int:
    """
    The algorithm of heuristic.
    1. Find the largest number of red chess
    2. spread this red chess directly to the blue chess start from the largest
    3. repeat 1 and 2 until there are no more blue chess left
    4. The number of operation is the result of heuristic
    """

    redChess: list[tuple] = []
    blueChess: list[tuple] = []
    result = 0
    for chess in chessBoard.values():
        redChess.append(chess) if chess[0] == "r" else blueChess.append(chess)
    redChess.sort(key=lambda x: x[1], reverse=True)
    blueChess.sort(key=lambda x: x[1])
    '''
    Put everything chess into list of redChess and blueChess separately, and sort them. 
    redChess sort from largest to smallest
    blueChess sort from smallest to largest
    '''

    while True:
        checkingChess = redChess[0]
        del redChess[0]
        result += 1
        for i in range(checkingChess[1]):
            if len(blueChess) == 0:
                return result
            changeChess = ("r", addition(blueChess.pop()[1]))
            if changeChess[1] != 0:
                if len(redChess) == 0 or changeChess[1] <= redChess[-1][1]:
                    redChess.append(changeChess)
                else:
                    if changeChess[1] <= redChess[-1][1]:
                        redChess.append(changeChess)
                    for chess in redChess:
                        if changeChess[1] > chess[1]:
                            redChess.insert(redChess.index(chess), changeChess)
                            break


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).

    # print(render_board(input, ansi=False))
    # print(heuristic(input))

    returnPath: list[tuple] = []
    # this dict store cost value and last node in the linked list with this cost
    indexDict: dict[int, BoardNode] = {}
    # initialize root node
    currentNode = BoardNode(input, None)

    while not currentNode.win():
        # print("1\n")
        # find all red chess on current board
        for nodeKey, nodeValue in currentNode.board.items():
            if nodeValue[0] == "r":
                # spread it in 6 directions
                for direction in moveDirection.keys():
                    # creat child node and set its values
                    childBoard = single_spread(currentNode.board, nodeKey, direction)
                    childNode = BoardNode(childBoard, currentNode)
                    childNode.level = currentNode.level + 1
                    childNode.cost = childNode.level + heuristic(childNode.board)
                    childNode.changeDirection = moveDirection[direction]
                    childNode.changePosition = nodeKey
                    # insert it in after the last node with the same cost in the linked list if it exists
                    if indexDict.__contains__(childNode.cost):
                        # set the last and next node of child node
                        childNode.lastNode = indexDict.get(childNode.cost)
                        childNode.nextNode = indexDict.get(childNode.cost).nextNode
                        # set next node's last node to child node if it exists
                        if indexDict.get(childNode.cost).nextNode is not None:
                            indexDict.get(childNode.cost).nextNode.lastNode = childNode
                        # set last node's next node to child node
                        indexDict.get(childNode.cost).nextNode = childNode
                        # set index to last node with this cost to child node
                        indexDict[childNode.cost] = childNode
                    # if this is the first node with this cost, check if there are node with 1 less cost
                    elif indexDict.__contains__(childNode.cost - 1):
                        # set the last and next node of child node
                        childNode.lastNode = indexDict.get(childNode.cost - 1)
                        childNode.nextNode = indexDict.get(childNode.cost - 1).nextNode
                        # set next node's last node to child node if it exists
                        if indexDict.get(childNode.cost - 1).nextNode is not None:
                            indexDict.get(childNode.cost - 1).nextNode.lastNode = childNode
                        # set last node's next node to child node
                        indexDict.get(childNode.cost - 1).nextNode = childNode
                        # set index to last node with this cost to child node
                        indexDict[childNode.cost] = childNode
                    else:
                        nextnode = currentNode.nextNode
                        while nextnode is not None and nextnode.cost <= childNode.cost:
                            nextnode = nextnode.nextNode
                        if nextnode is not None:
                            # set the last and next node of child node
                            childNode.lastNode = nextnode.lastNode
                            childNode.nextNode = nextnode
                            # set last node's next node to child node if it exists
                            if nextnode.lastNode is not None:
                                nextnode.lastNode.nextNode = childNode
                            # set next node's last node to child node
                            nextnode.lastNode = childNode
                            # set index to last node with this cost to child node
                            indexDict[childNode.cost] = childNode
                        else:
                            # link child node and parent node
                            childNode.lastNode = currentNode
                            currentNode.nextNode = childNode
                            # set index to last node with this cost to child node
                            indexDict[childNode.cost] = childNode

        currentNode = currentNode.nextNode

    # print(render_board(currentNode.board, ansi=False))
    result = []
    while currentNode.level != 0:
        if len(result) == 0:
            result.append(currentNode.getOutCome())
        else:
            result.insert(0, currentNode.getOutCome())
        currentNode = currentNode.parentNode

    return result





    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    '''return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]'''
