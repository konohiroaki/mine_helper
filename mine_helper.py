import win32api
import win32con

from PIL import ImageGrab
from pywinauto import findwindows
from pywinauto.controls.HwndWrapper import HwndWrapper

import mine_solver
from mine_const import Const


def main():
    hwnd = HwndWrapper(findwindows.find_windows(class_name="ThunderRT6FormDC", title="Minesweeper X")[0])
    while True:
        board = get_board(hwnd)
        status = mine_solver.get_board_status(board)
        if status is Const.BoardStatus.BURST:
            # break
            reset_board(hwnd)
            continue
        result_list = mine_solver.solve(board)
        action(hwnd, result_list)
        if len(result_list) == 0:
            break


def get_board(hwnd):
    rect = hwnd.ClientAreaRect()
    img = ImageGrab.grab((rect.left + Const.Padding.LEFT, rect.top + Const.Padding.TOP,
                          rect.right - Const.Padding.RIGHT, rect.bottom - Const.Padding.BOTTOM))

    width = int(img.width / Const.CellSize.WIDTH)
    height = int(img.height / Const.CellSize.HEIGHT)

    result_board = []
    for y in range(0, height):
        result_board.append([])
        for x in range(0, width):
            cell = __get_cell(img, y, x)
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
    height = len(board)
    width = len(board[0])
    for y in range(height):
        if y is not 0:
            print()
        for x in range(width):
            print(board[y][x][1], end="")


def reset_board(hwnd):
    hwnd.MenuSelect("Game->New")


def action(hwnd, action_list):
    rect = hwnd.ClientAreaRect()
    for each in action_list:
        x = rect.left + Const.Padding.LEFT + each["coord"][1] * Const.CellSize.WIDTH
        y = rect.top + Const.Padding.TOP + each["coord"][0] * Const.CellSize.HEIGHT
        if each["type"] == Const.CellAction.OPEN:
            __open(x, y)
        else:
            __flag(x, y)


def __open(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def __flag(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


if __name__ == "__main__":
    main()
