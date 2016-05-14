"""Solves Minesweeper.

Receives: A board[][].
Returns: A list of cell & action indicating where you can open/flag.
"""

from mine_const import Const
import random


def solve(board):
    result_list = []
    board_status = get_board_status(board)
    if board_status is Const.BoardStatus.START:
        result_list += __guess(board)
    elif board_status is Const.BoardStatus.MIDSTREAM:
        result_list += __solve_by_single(board)
        if len(result_list) is 0:
            result_list += __solve_by_double(board)
        if len(result_list) is 0:
            result_list += __guess(board)
    return result_list


def get_board_status(board):
    if __count_cell_with(board, Const.Cell.BURST) is not 0:
        return Const.BoardStatus.BURST
    elif __count_cell_with(board, Const.Cell.CLOSED) is 0:
        return Const.BoardStatus.END
    elif __count_cell_with(board, Const.Cell.ZERO) is not 0:
        return Const.BoardStatus.MIDSTREAM
    else:
        return Const.BoardStatus.START


def __count_cell_with(board, status):
    count = 0
    for y, x in ((y, x) for y in range(len(board)) for x in range(len(board[0]))):
        if board[y][x] is status:
            count += 1
    return count


def __get_cell_with(board, status):
    cell_list = []
    for y, x in ((y, x) for y in range(len(board)) for x in range(len(board[0]))):
        if board[y][x] is status:
            cell_list.append([y, x])
    return cell_list


def __solve_by_single(board):
    """Solve the board only by referring single cell.

    If a number cell
        1. has exactly same number of CLOSED cells around, then all of them can be FLAGGED
        2. is zero, all cells around can be OPENED.
    A "number" is actually (shown number - flags around)
    """
    result_list = []
    for y, x in ((y, x) for y in range(len(board)) for x in range(len(board[0]))):
        if __is_number(board[y][x]):
            closed = __get_cell_around(board, y, x, Const.Cell.CLOSED)
            real_number = __get_real_number(board, y, x)
            if real_number == len(closed) != 0:
                for cell in closed:
                    result_list.append({"type": Const.CellAction.FLAG, "coord": (cell[0], cell[1])})
            elif real_number == 0:
                for cell in closed:
                    result_list.append({"type": Const.CellAction.OPEN, "coord": (cell[0], cell[1])})
    return list({v["coord"]: v for v in result_list}.values())


def __is_number(cell):
    if (cell == Const.Cell.ONE or cell == Const.Cell.TWO or cell == Const.Cell.THREE
        or cell == Const.Cell.FOUR or cell == Const.Cell.FIVE or cell == Const.Cell.SIX
        or cell == Const.Cell.SEVEN or cell == Const.Cell.EIGHT):
        return True
    else:
        return False


def __get_cell_around(board, y, x, cell_type):
    cell_list = []
    for yy, xx in ((y + ymargin, x + xmargin) for ymargin in (-1, 0, 1) for xmargin in (-1, 0, 1)):
        if (__is_around(len(board), len(board[0]), (y, x), (yy, xx))
            and board[yy][xx][0] is cell_type[0]):
            cell_list.append((yy, xx))
    return cell_list


def __get_real_number(board, y, x):
    return board[y][x][0] - len(__get_cell_around(board, y, x, Const.Cell.FLAGGED))


def __solve_by_double(board):
    """Solve the board by comparing with neighbor cell.

    If abs(a number cell - its neighbor number cell) is same as either's non-shared cells count, those non-shared
    cells will be determined.
        1. If the subtracted value is positive, non-shared cells for the cell can be FLAGGED.
        2. If the subtracted value is negative, non-shared cells for the cell can be OPENED.
    """
    result_list = []
    for y, x in ((y, x) for y in range(len(board)) for x in range(len(board[0])) if __is_number((board[y][x]))):
        for yy, xx in ((y + ymargin, x + xmargin) for ymargin in (-1, 0, 1) for xmargin in (-1, 0, 1)):
            if __is_around(len(board), len(board[0]), (y, x), (yy, xx)) and board[yy][xx] == Const.Cell.CLOSED:
                for yyy, xxx in ((yy + ymargin, xx + xmargin) for ymargin in (-1, 0, 1) for xmargin in (-1, 0, 1)):
                    if __is_around(len(board), len(board[0]), (yy, xx), (yyy, xxx)) and __is_number(board[yyy][xxx]) \
                            and not (yyy == y and xxx == x):
                        yx_cells = __get_cell_around(board, y, x, Const.Cell.CLOSED)
                        yyxx_cells = __get_cell_around(board, yyy, xxx, Const.Cell.CLOSED)
                        diff = __get_real_number(board, y, x) - __get_real_number(board, yyy, xxx)
                        non_shared = list(set(yx_cells) - set(yyxx_cells))
                        rev_non_shared = list(set(yyxx_cells) - set(yx_cells))
                        if len(non_shared) == diff:
                            for cell in non_shared:
                                result_list.append({"type": Const.CellAction.FLAG, "coord": (cell[0], cell[1])})
                        elif len(non_shared) == abs(diff) and len(rev_non_shared) == len(non_shared):
                            for cell in non_shared:
                                result_list.append({"type": Const.CellAction.OPEN, "coord": (cell[0], cell[1])})
                        elif len(rev_non_shared) == 0 and diff == 0:
                            for cell in non_shared:
                                result_list.append({"type": Const.CellAction.OPEN, "coord": (cell[0], cell[1])})
    return list({v["coord"]: v for v in result_list}.values())


def __is_around(height, width, cell, neighbor):
    return (not (cell[0] == neighbor[0] and cell[1] == neighbor[1])
            and 0 <= neighbor[0] < height and 0 <= neighbor[1] < width)


def __guess(board):
    """Choose one randomly from CLOSED cells."""
    if len(__get_cell_with(board, Const.Cell.CLOSED)) < 500:
        return []
    closed = __get_cell_with(board, Const.Cell.CLOSED)
        return [{"type": Const.CellAction.OPEN, "coord": closed[random.randrange(len(closed))]}]
