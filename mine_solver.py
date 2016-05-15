"""Solves Minesweeper.

Receives: A board[][].
Returns: A list of cell & action indicating where you can open/flag.
"""

from mine_const import Const
import random


def solve(board):
    results = []
    board_status = get_board_status(board)
    if board_status == Const.BoardStatus.START:
        results += __guess(board)
    elif board_status == Const.BoardStatus.MIDSTREAM:
        results += __solve_by_single(board)
        results += __solve_by_double(board)
        if len(results) == 0:
            results += __guess(board)
    return list({v["coord"]: v for v in results}.values())


def get_board_status(board):
    if len(__get_with(board, Const.Cell.BURST)) != 0:
        return Const.BoardStatus.BURST
    elif len(__get_with(board, Const.Cell.CLOSED)) == 0:
        return Const.BoardStatus.END
    elif len(__get_with(board, Const.Cell.ZERO)) != 0:
        return Const.BoardStatus.MIDSTREAM
    else:
        return Const.BoardStatus.START


def __get_with(board, cell_type):
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))
    return [(y, x) for y, x in coordinates if board[y][x] == cell_type]


def __solve_by_single(board):
    """Solve the board only by referring single cell.

    If a number cell
        1. has exactly same number of CLOSED cells around, then all of them can be FLAGGED
        2. is zero, all cells around can be OPENED.
    A "number" is actually (shown number - flags around)
    """
    results = []
    coordinates = ((y, x) for y in range(len(board)) for x in range(len(board[0])))
    number_coords = ((y, x) for y, x in coordinates if __is_number(board[y][x]))

    for y, x in number_coords:
        closed = __get_around_with(board, y, x, Const.Cell.CLOSED)
        real_number = __get_real_number(board, y, x)

        if real_number == len(closed) != 0:
            for cell in closed:
                results.append({"type": Const.CellAction.FLAG, "coord": cell})
        elif real_number == 0:
            for cell in closed:
                results.append({"type": Const.CellAction.OPEN, "coord": cell})

    return list({v["coord"]: v for v in results}.values())


def __is_number(cell):
    return Const.Cell.ZERO < cell <= Const.Cell.EIGHT


def __get_board_size(board):
    return len(board), len(board[0])


def __get_around(board, y, x):
    board_size = __get_board_size(board)
    margins = ((ym, xm) for ym in (-1, 0, 1) for xm in (-1, 0, 1) if not ym == xm == 0)
    return [(y + ym, x + xm) for ym, xm in margins if __is_inside(board_size, (y + ym, x + xm))]


def __get_around_with(board, y, x, cell_type):
    around = __get_around(board, y, x)
    return [(yy, xx) for yy, xx in around if board[yy][xx] == cell_type]


def __get_real_number(board, y, x):
    return board[y][x][0] - len(__get_around_with(board, y, x, Const.Cell.FLAGGED))


def __solve_by_double(board):
    """Solve the board by comparing with neighbor cell.

    y1
    If (a number cell - its neighbor number cell which shares a 1 or more CLOSED cells) is same as either's non-shared
    cells
    count,
    those non-shared
    cells will be determined.
        1. If the subtracted value is positive, non-shared cells for the cell can be FLAGGED.
        2. If the subtracted value is negative, non-shared cells for the cell can be OPENED.
    """
    results = []
    c1_list = ((y, x) for y in range(len(board)) for x in range(len(board[0])) if __is_number(board[y][x]))

    for y1, x1 in c1_list:
        c1_around = __get_around_with(board, y1, x1, Const.Cell.CLOSED)
        c2_list = [(y2, x2) for yy, xx in c1_around for y2, x2 in __get_around(board, yy, xx)
                   if __is_number(board[y2][x2]) if not (y1 == y2 and x1 == x2)]

        for y2, x2 in c2_list:
            c2_around = __get_around_with(board, y2, x2, Const.Cell.CLOSED)
            c1_non_shared = list(set(c1_around) - set(c2_around))
            c2_non_shared = list(set(c2_around) - set(c1_around))
            diff = __get_real_number(board, y1, x1) - __get_real_number(board, y2, x2)
            if len(c1_non_shared) == diff:
                for cell in c1_non_shared:
                    results.append({"type": Const.CellAction.FLAG, "coord": cell})
            elif len(c1_non_shared) == -diff and len(c2_non_shared) == len(c1_non_shared):
                for cell in c1_non_shared:
                    results.append({"type": Const.CellAction.OPEN, "coord": cell})
            elif len(c2_non_shared) == 0 and diff == 0:
                for cell in c1_non_shared:
                    results.append({"type": Const.CellAction.OPEN, "coord": cell})
    return list({v["coord"]: v for v in results}.values())


def __is_inside(board_size, neighbor_coord):
    return 0 <= neighbor_coord[0] < board_size[0] and 0 <= neighbor_coord[1] < board_size[1]


def __is_inside_with(board, neighbor_coord, cell_type):
    board_size = __get_board_size(board)

    return __is_inside(board_size, neighbor_coord) and board[neighbor_coord[0]][neighbor_coord[1]] == cell_type


def __guess(board):
    """Choose one randomly from CLOSED cells."""
    if len(__get_with(board, Const.Cell.CLOSED)) < 500:
        return []
    closed = __get_with(board, Const.Cell.CLOSED)
    return [{"type": Const.CellAction.OPEN, "coord": closed[random.randrange(len(closed))]}]
