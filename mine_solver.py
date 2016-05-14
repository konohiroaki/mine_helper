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
    if __count_with(board, Const.Cell.BURST) is not 0:
        return Const.BoardStatus.BURST
    elif __count_with(board, Const.Cell.CLOSED) is 0:
        return Const.BoardStatus.END
    elif __count_with(board, Const.Cell.ZERO) is not 0:
        return Const.BoardStatus.MIDSTREAM
    else:
        return Const.BoardStatus.START


def __count_with(board, cell_type):
    count = 0
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))
    for _ in ((y, x) for y, x in coordinates if board[y][x] is cell_type):
        count += 1
    return count


def __get_with(board, cell_type):
    result_list = []
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))

    for y, x in ((y, x) for y, x in coordinates if board[y][x] is cell_type):
        result_list.append([y, x])
    return result_list


def __solve_by_single(board):
    """Solve the board only by referring single cell.

    If a number cell
        1. has exactly same number of CLOSED cells around, then all of them can be FLAGGED
        2. is zero, all cells around can be OPENED.
    A "number" is actually (shown number - flags around)
    """
    result_list = []
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))

    for y, x in ((y, x) for y, x in coordinates if __is_number(board[y][x])):
        closed = __get_around_with(board, y, x, Const.Cell.CLOSED)
        real_number = __get_real_number(board, y, x)

        if real_number == len(closed) != 0:
            for cell in closed:
                result_list.append({"type": Const.CellAction.FLAG, "coord": cell})
        elif real_number == 0:
            for cell in closed:
                result_list.append({"type": Const.CellAction.OPEN, "coord": cell})

    return list({v["coord"]: v for v in result_list}.values())


def __is_number(cell):
    if (cell == Const.Cell.ONE or cell == Const.Cell.TWO or cell == Const.Cell.THREE
        or cell == Const.Cell.FOUR or cell == Const.Cell.FIVE or cell == Const.Cell.SIX
        or cell == Const.Cell.SEVEN or cell == Const.Cell.EIGHT):
        return True
    else:
        return False


def __get_board_size(board):
    return len(board), len(board[0])


def __get_around_with(board, y, x, cell_type):
    result_list = []
    margin_list = ((ym, xm) for ym in (-1, 0, 1) for xm in (-1, 0, 1) if not ym == xm == 0)

    for yy, xx in ((y + ym, x + xm) for ym, xm in margin_list if __is_around_with(board, (y + ym, x + xm), cell_type)):
        result_list.append((yy, xx))
    return result_list


def __get_real_number(board, y, x):
    return board[y][x][0] - len(__get_around_with(board, y, x, Const.Cell.FLAGGED))


def __solve_by_double(board):
    """Solve the board by comparing with neighbor cell.

    If abs(a number cell - its neighbor number cell) is same as either's non-shared cells count, those non-shared
    cells will be determined.
        1. If the subtracted value is positive, non-shared cells for the cell can be FLAGGED.
        2. If the subtracted value is negative, non-shared cells for the cell can be OPENED.
    """
    result_list = []
    board_size = __get_board_size(board)
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))
    margins = [(ym, xm) for ym in (-1, 0, 1) for xm in (-1, 0, 1) if not ym == xm == 0]

    for y1, x1 in ((y, x) for y, x in coordinates if __is_number((board[y][x]))):
        for yy, xx in ((y1 + ym, x1 + xm) for ym, xm in margins
                       if __is_around_with(board, (y1 + ym, x1 + xm), Const.Cell.CLOSED)):
            for y2, x2 in ((yy + ym, xx + xm) for ym, xm in margins if __is_around(board_size, (yy + ym, xx + xm))):
                if __is_number(board[y2][x2]) and not (y1 == y2 and x1 == x2):
                    c1_around = __get_around_with(board, y1, x1, Const.Cell.CLOSED)
                    c2_around = __get_around_with(board, y2, x2, Const.Cell.CLOSED)
                    c1_non_shared = list(set(c1_around) - set(c2_around))
                    c2_non_shared = list(set(c2_around) - set(c1_around))
                    diff = __get_real_number(board, y1, x1) - __get_real_number(board, y2, x2)
                    if len(c1_non_shared) == diff:
                        for cell in c1_non_shared:
                            result_list.append({"type": Const.CellAction.FLAG, "coord": cell})
                    elif len(c1_non_shared) == -diff and len(c2_non_shared) == len(c1_non_shared):
                        for cell in c1_non_shared:
                            result_list.append({"type": Const.CellAction.OPEN, "coord": cell})
                    elif len(c2_non_shared) == 0 and diff == 0:
                        for cell in c1_non_shared:
                            result_list.append({"type": Const.CellAction.OPEN, "coord": cell})
    return list({v["coord"]: v for v in result_list}.values())


def __is_around(board_size, neighbor_cell):
    return 0 <= neighbor_cell[0] < board_size[0] and 0 <= neighbor_cell[1] < board_size[1]


def __is_around_with(board, neighbor_cell, cell_type):
    board_size = __get_board_size(board)
    return __is_around(board_size, neighbor_cell) and board[neighbor_cell[0]][neighbor_cell[1]] == cell_type


def __guess(board):
    """Choose one randomly from CLOSED cells."""
    if len(__get_with(board, Const.Cell.CLOSED)) < 500:
        return []
    closed = __get_with(board, Const.Cell.CLOSED)
    return [{"type": Const.CellAction.OPEN, "coord": closed[random.randrange(len(closed))]}]
