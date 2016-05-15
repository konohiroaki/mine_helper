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
        results += __guess(board, board_status)
    elif board_status == Const.BoardStatus.MIDSTREAM:
        results += __solve_by_single(board)
        results += __solve_by_double(board)
        if len(results) == 0:
            results += __guess(board, board_status)
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
    """Solve the board only by referring single number cell.

        A   B   C
      +-----------+
    a | 1 | 1 | 1 |
      |---|---|---|
    b | 1 | ? | ? |
      +-----------+

    ::How to solve by single::
    1. When coord->"aA":
        There is only "bB" CLOSED around, Thus "bB" can be FLAGGED.
    2. When After 1. coord->aB:
        There is a flag on "bB". Thus "bC" can be OPENED.
    """
    results = []
    number_coords = ((y, x) for y in range(len(board)) for x in range(len(board[0])) if __is_number(board[y][x]))

    for coord in number_coords:
        around = __get_around_with(board, coord, Const.Cell.CLOSED)
        real_number = __get_real_number(board, coord)

        if real_number == len(around) != 0:
            results += [{"type": Const.CellAction.FLAG, "coord": coord} for coord in around]
        elif real_number == 0:
            results += [{"type": Const.CellAction.OPEN, "coord": coord} for coord in around]

    return list({v["coord"]: v for v in results}.values())


def __is_number(cell):
    return Const.Cell.ZERO[0] < cell[0] <= Const.Cell.EIGHT[0]


def __get_board_size(board):
    return len(board), len(board[0])


def __get_around(board, coord):
    y, x = coord
    board_size = __get_board_size(board)
    margins = ((ym, xm) for ym in (-1, 0, 1) for xm in (-1, 0, 1) if not ym == xm == 0)
    return [(y + ym, x + xm) for ym, xm in margins if __is_inside(board_size, (y + ym, x + xm))]


def __get_around_with(board, coord, cell_type):
    around = __get_around(board, coord)
    return [(yy, xx) for yy, xx in around if board[yy][xx] == cell_type]


def __get_real_number(board, coord):
    return board[coord[0]][coord[1]][0] - len(__get_around_with(board, coord, Const.Cell.FLAGGED))


def __solve_by_double(board):
    """Solve the board by referring two number cells.

        A   B   C   D
      +---------------+
    a | 1 | 1 | 2 | 1 |
      |---|---|---|---|
    b | ? | ? | ? | ? |
      +---------------+

    ::Word Definition::
    c1: A coordinate of a number cell.
    c2: A coordinate of a number cell positioned NEARBY c1.
    NEARBY: A place which has at least one shared linked CLOSED cell.

    ::How to solve by double::
    1. When c1->"aB", c2->"aA":
        According to "aA", there is a mine in "bA or "bB", Thus "bC" can be OPENED.
    2. When c1->"aB", c2->"aC":
        According to "aC", there is a mine in "bB or "bC". Thus "bA" can be OPENED.
    3. When c1->"aC", c2->"aB":
        According to "aB", there is only one mine in "bB" and "bC" at most. Thus "bD" can be FLAGGED.
    """
    results = []
    c1_list = ((y, x) for y in range(len(board)) for x in range(len(board[0])) if __is_number(board[y][x]))

    for c1 in c1_list:
        y1, x1 = c1
        c1_around = set(__get_around_with(board, c1, Const.Cell.CLOSED))
        c2_list = ((y2, x2) for yy, xx in c1_around for y2, x2 in __get_around(board, (yy, xx))
                   if __is_number(board[y2][x2]) if not (y1 == y2 and x1 == x2))

        for c2 in c2_list:
            c2_around = set(__get_around_with(board, c2, Const.Cell.CLOSED))
            c1_non_shared = c1_around - c2_around
            c2_non_shared = c2_around - c1_around
            diff = __get_real_number(board, c1) - __get_real_number(board, c2)

            if len(c1_non_shared) == diff:
                results += [{"type": Const.CellAction.FLAG, "coord": coord} for coord in c1_non_shared]
            elif len(c1_non_shared) == -diff and len(c2_non_shared) == len(c1_non_shared):
                results += [{"type": Const.CellAction.OPEN, "coord": coord} for coord in c1_non_shared]
            elif len(c2_non_shared) == 0 and diff == 0:
                results += [{"type": Const.CellAction.OPEN, "coord": coord} for coord in c1_non_shared]

    return list({v["coord"]: v for v in results}.values())


def __is_inside(board_size, coord):
    return 0 <= coord[0] < board_size[0] and 0 <= coord[1] < board_size[1]


def __is_inside_with(board, coord, cell_type):
    board_size = __get_board_size(board)
    return __is_inside(board_size, coord) and board[coord[0]][coord[1]] == cell_type


def __guess(board, board_status):
    """Choose one randomly from CLOSED cells."""

    if board_status == Const.BoardStatus.START:
        closed = __get_with(board, Const.Cell.CLOSED)
        return [{"type": Const.CellAction.OPEN, "coord": closed[random.randrange(len(closed))]}]
    elif len(__get_with(board, Const.Cell.CLOSED)) < 200:
        return []
    else:
        return __get_least_prob(board)


def __get_least_prob(board):
    number_coords = ((y, x) for y in range(len(board)) for x in range(len(board[0])) if __is_number(board[y][x]))

    least_prob = 1
    result = None
    for coord in number_coords:
        real_number = __get_real_number(board, coord)
        if real_number != 0:
            around = __get_around_with(board, coord, Const.Cell.CLOSED)
            prob = real_number / len(around)
            if prob < least_prob:
                least_prob = prob
                result = around[random.randrange(len(around))]
    return [{"type": Const.CellAction.OPEN, "coord": result}]
