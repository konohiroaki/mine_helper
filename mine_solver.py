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
            real_number = board[y][x][0] - len(__get_cell_around(board, y, x, Const.Cell.FLAGGED))
            if real_number == len(closed) != 0:
                for cell in closed:
                    if {"type": Const.CellAction.FLAG, "coord": [cell[0], cell[1]]} not in result_list:
                        result_list.append({"type": Const.CellAction.FLAG, "coord": [cell[0], cell[1]]})
            elif real_number == 0:
                for cell in closed:
                    if {"type": Const.CellAction.OPEN, "coord": [cell[0], cell[1]]} not in result_list:
                        result_list.append({"type": Const.CellAction.OPEN, "coord": [cell[0], cell[1]]})
    return result_list


def __is_number(cell):
    if (cell == Const.Cell.ONE or cell == Const.Cell.TWO or cell == Const.Cell.THREE
        or cell == Const.Cell.FOUR or cell == Const.Cell.FIVE or cell == Const.Cell.SIX
        or cell == Const.Cell.SEVEN or cell == Const.Cell.EIGHT):
        return True
    else:
        return False


def __get_cell_around(board, y, x, cell_type):
    cell_list = []
    for yyy, xxx in ((yy + y, xx + x) for yy in (-1, 0, 1) for xx in (-1, 0, 1)):
        if (not (yyy == y and xxx == x)
            and 0 <= yyy < len(board) and 0 <= xxx < len(board[0])
            and board[yyy][xxx][0] is cell_type[0]):
            cell_list.append((yyy, xxx))
    return cell_list


def __solve_by_double(board):
    """Solve the board by comparing with neighbor cell.

    If abs(a number cell - its neighbor number cell) is same as either's non-shared cells count, those non-shared
    cells will be determined.
        1. If the subtracted value is positive, non-shared cells for the cell can be FLAGGED.
        2. If the subtracted value is negative, non-shared cells for the cell can be OPENED.
    """
    return []


def __guess(board):
    """Choose one randomly from CLOSED cells."""
    closed = __get_cell_with(board, Const.Cell.CLOSED)
    return [{"type": Const.CellAction.OPEN, "coord": closed[random.randrange(len(closed))]}]
