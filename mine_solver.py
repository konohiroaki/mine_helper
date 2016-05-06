"""
Solves Minesweeper.
Receives a board[][] and returns a list of cell & action indicating where we can open/flag.
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
    for y, row in enumerate(board):
        for x, cell in enumerate(board[y]):
            if board[y][x] is status:
                count += 1
    return count


def __get_cell_with(board, status):
    cell_list = []
    for y, row in enumerate(board):
        for x, cell in enumerate(board[y]):
            if board[y][x] is status:
                cell_list.append([y, x])
    return cell_list


def __solve_by_single(board):
    # if subtract_flags(board[y][x])# +  == #旗なしclosed - 畑ありclosed
    # if cellの数字が周りのclosed-floaggedと同じだったら、全部旗つけ
    # if 上のを終えて、cellの周りの旗がcellと同じ数になったら、全部開く
    # listにattach
    list = []
    for y, row in enumerate(board):
        for x, cell in enumerate(board[y]):
            if __is_number(board[y][x]):
                closed = __get_cell_around(board, y, x, Const.Cell.CLOSED)
                real_number = board[y][x][0] - len(__get_cell_around(board, y, x, Const.Cell.FLAGGED))
                if real_number == len(closed) != 0:
                    for cell in closed:
                        if {"type": Const.CellAction.FLAG, "coord": [cell[0], cell[1]]} not in list:
                            list.append({"type": Const.CellAction.FLAG, "coord": [cell[0], cell[1]]})
                elif real_number == 0:
                    for cell in closed:
                        if {"type": Const.CellAction.OPEN, "coord": [cell[0], cell[1]]} not in list:
                            list.append({"type": Const.CellAction.OPEN, "coord": [cell[0], cell[1]]})
    return list


def __is_number(cell):
    if (cell == Const.Cell.ONE or cell == Const.Cell.TWO
        or cell == Const.Cell.THREE or cell == Const.Cell.FOUR or cell == Const.Cell.FIVE
        or cell == Const.Cell.SIX or cell == Const.Cell.SEVEN or cell == Const.Cell.EIGHT):
        return True
    else:
        return False


def __get_cell_around(board, y, x, cell_type):
    cell_list = []
    for yy in (-1, 0, 1):
        for xx in (-1, 0, 1):
            if (not (yy is 0 and xx is 0)
                and 0 <= y + yy < len(board)
                and 0 <= x + xx < len(board[0])
                and board[y + yy][x + xx][0] is cell_type[0]):
                cell_list.append([y + yy, x + xx])
    return cell_list


def __solve_by_double(board):
    # 隣り合う数字同士の差分と同じだけどちらかだけに隣接する未開放のセルがあれば、そこは確定する
    return []


def __guess(board):
    # 確率が一番少ないやつ適当にチョイス、あるいは0がなければ完全ランダムに。
    closed = __get_cell_with(board, Const.Cell.CLOSED)
    return [{"type": Const.CellAction.OPEN,
             "coord": closed[random.randrange(len(closed))]}]
