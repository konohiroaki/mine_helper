from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.controls.HwndWrapper import HwndWrapper
from PIL import ImageGrab
from mine_const import Const
import mine_solver
import time


def main():
    hwnd = findwindows.find_windows(class_name="ThunderRT6FormDC", title="Minesweeper X")[0]
    app = get_app(hwnd)
    hwndw = HwndWrapper(hwnd)
    while True:
        board = get_board(app)
        status = mine_solver.get_board_status(board)
        if status is Const.BoardStatus.BURST:
            reset_board(app)
            continue
        result_list = mine_solver.solve(board)
        action(hwndw, result_list)
        if len(result_list) == 0:
            break


def get_board(app):
    rect = app.MinesweeperX.ClientAreaRect()
    img = ImageGrab.grab((rect.left + Const.Padding.LEFT, rect.top + Const.Padding.TOP,
                          rect.right - Const.Padding.RIGHT, rect.bottom - Const.Padding.BOTTOM))

    width = int(img.width / Const.CellSize.WIDTH)
    height = int(img.height / Const.CellSize.HEIGHT)

    result_board = []
    for y in range(0, height):
        result_board.append([])
        for x in range(0, width):
            cell = __get_cell(img, y, x)
            if cell is None:
                pass
            result_board[y].append(cell)
    return result_board


def __get_cell(img, y, x):
    pos1 = __get_pixel(img, y, x, 0)
    if pos1 == Const.Color.BURST:
        return Const.Cell.BURST
    elif pos1 == Const.Color.ZERO[0]:
        pos2 = __get_pixel(img, y, x, 1)
        if pos2 == Const.Color.ZERO[1]:
            pos3 = __get_pixel(img, y, x, 2)
            if pos3 == Const.Color.ZERO[2]:
                return Const.Cell.ZERO
            elif pos3 == Const.Color.MINE[2]:
                return Const.Cell.MINE
            elif pos3 == Const.Color.WRONG_FLAG[2]:
                return Const.Cell.WRONG_FLAG
        elif pos2 == Const.Color.ONE[1]:
            return Const.Cell.ONE
        elif pos2 == Const.Color.TWO[1]:
            return Const.Cell.TWO
        elif pos2 == Const.Color.THREE[1]:
            return Const.Cell.THREE
        elif pos2 == Const.Color.FOUR[1]:
            return Const.Cell.FOUR
        elif pos2 == Const.Color.FIVE[1]:
            return Const.Cell.FIVE
        elif pos2 == Const.Color.SIX[1]:
            return Const.Cell.SIX
        elif pos2 == Const.Color.SEVEN[1]:
            return Const.Cell.SEVEN
        elif pos2 == Const.Color.EIGHT[1]:
            return Const.Cell.EIGHT
    elif pos1 == Const.Color.CLOSED[0]:
        pos2 = __get_pixel(img, y, x, 1)
        if pos2 == Const.Color.CLOSED[1]:
            pos3 = __get_pixel(img, y, x, 2)
            if pos3 == Const.Color.CLOSED[2]:
                return Const.Cell.CLOSED
            elif pos3 == Const.Color.FLAGGED[2]:
                return Const.Cell.FLAGGED
        elif pos2 == Const.Color.QUESTION[1]:
            return Const.Cell.QUESTION


def __get_pixel(img, y, x, idx):
    return img.getpixel((Const.CellSize.WIDTH * x + Const.Color.POSITION[idx]["X"],
                         Const.CellSize.HEIGHT * y + Const.Color.POSITION[idx]["Y"]))


def output(board):
    str_board = __stringify_board(board)
    for y, rrr in enumerate(str_board):
        print()
        for x, ccc in enumerate(rrr):
            print(str_board[y][x], end="")


def __stringify_board(board):
    str_board = []
    for y, row in enumerate(board):
        str_board.append([])
        for x, cell in enumerate(row):
            str_board[y].append(board[y][x][1])
    return str_board


def reset_board(app):
    app.MinesweeperX.MenuSelect("Game->New")


def action(hwnd, action_list):
    for each in action_list:
        if each["type"] == Const.CellAction.OPEN:
            __open(hwnd, each["coord"][0], each["coord"][1])
        else:
            __flag(hwnd, each["coord"][0], each["coord"][1])


def __open(hwndw, y, x):
    hwndw.Click(coords=(Const.CellSize.WIDTH * x + Const.Padding.LEFT,
                        Const.CellSize.HEIGHT * y + Const.Padding.TOP))


def __flag(hwndw, y, x):
    hwndw.RightClick(coords=(Const.CellSize.WIDTH * x + Const.Padding.LEFT,
                             Const.CellSize.HEIGHT * y + Const.Padding.TOP))


def get_app(hwnd):
    app = Application()
    app.connect(handle=hwnd)
    return app


if __name__ == "__main__":
    main()
