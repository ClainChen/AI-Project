# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board

"""
The Dictionary which stores the move method
Key is the string which describe the direction of movement
Value is the coordinate translation which store with tuple
"""
moveDirection: dict[str, tuple[int, int]] = {
    "up": (1, -1),
    "down": (-1, 1),
    "right up": (1, 0),
    "right down": (0, 1),
    "left up": (0, -1),
    "left down": (-1, 0)
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
    redChess: list[tuple] = []
    blueChess: list[tuple] = []
    result = 0
    for chess in chessBoard.values():
        redChess.append(chess) if chess[0] == "r" else blueChess.append(chess)
    redChess.sort(key=lambda x: x[1], reverse=True)
    blueChess.sort(key=lambda x: x[1])

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
    print(render_board(input, ansi=False))
    print(heuristic(input))

    # count = 1
    # for each in newBoards:
    #     print(count, "---------------------")
    #     print(each)
    #     print(render_board(each, ansi=False))
    #     count += 1

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
