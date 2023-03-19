#这个文件用来测试输出结果
#总而言之就是可以操作这个文件来debug

from sys import stdin
from program import search

def parse_input(input: str) -> dict[tuple, tuple]:
    """
    Parse input CSV into a dictionary of board cell states.
    """
    return {
        (int(r), int(q)): (p.strip(), int(k))
        for r, q, p, k in [
            line.split(',') for line in input.splitlines()
            if len(line.strip()) > 0
        ]
    }


def print_sequence(sequence: list[tuple]):
    """
    Print the given action sequence. All actions are prepended with the
    word "SPREAD", and each action is printed on a new line.
    """
    for r, q, dr, dq in sequence:
        print(f"SPREAD {r} {q} {dr} {dq}")


def LoadCSVFile() -> str:
    check = False

    while not check:
        try:
            fileAddress = input("请输入csv文件相对路径： ")
            file = open(fileAddress)
        except FileNotFoundError:
            print("无效路径！")
        else:
            print("文件获取成功")
            result = file.read()
            check = True

    return result

def main():
    """
    Main entry point for program.
    """

    print("请输入csv文件相对路径，推荐将csv文件放在此项目根目录中。")
    print("如项目给的默认csv文件名为test.csv，所以就输入 ../test.csv")
    initialBoard = LoadCSVFile()
    input = parse_input(initialBoard)
    sequence: list[tuple] = search(input)
    print_sequence(sequence)


if __name__ == "__main__":
    main()
