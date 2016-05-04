"""
Solves Minesweeper.
Receives a board[][] and returns a list of cell & action indicating where we can open/flag.
"""

from mine_const import Const
import random


def solve(board):
    result_list = []
    board_status = __get_board_status(board)
    print(board_status)
    if board_status == Const.BoardStatus.START:
        result_list += __guess(board)
    elif board_status == Const.BoardStatus.MIDSTREAM:
        result_list += __solve_by_single(board)
        if len(result_list) == 0:
            result_list += __solve_by_double(board)
        if len(result_list) == 0:
            result_list += __guess(board)
    return result_list


def __get_board_status(board):
    if __count_cell_with(board, Const.Cell.BURST) != 0:
        return Const.BoardStatus.BURST
    elif __count_cell_with(board, Const.Cell.CLOSED == 0):
        return Const.BoardStatus.END
    elif __count_cell_with(board, Const.Cell.ONE) != 0 \
            or __count_cell_with(board, Const.Cell.ONE) != 0 \
            or __count_cell_with(board, Const.Cell.TWO) != 0 \
            or __count_cell_with(board, Const.Cell.THREE) != 0 \
            or __count_cell_with(board, Const.Cell.FOUR) != 0 \
            or __count_cell_with(board, Const.Cell.FIVE) != 0 \
            or __count_cell_with(board, Const.Cell.SIX) != 0 \
            or __count_cell_with(board, Const.Cell.SEVEN) != 0 \
            or __count_cell_with(board, Const.Cell.EIGHT) != 0:
        return Const.BoardStatus.MIDSTREAM
    else:
        return Const.BoardStatus.START


def __count_cell_with(board, status):
    count = 0
    for y, row in enumerate(board):
        for x, cell in enumerate(board[y]):
            if board[y][x] == status:
                count += 1
    return count


def __solve_by_single(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(board[y]):
            pass
            # if cellの数字が周りのclosed-floaggedと同じだったら、全部旗つけ
            # if 上のを終えて、cellの周りの旗がcellと同じ数になったら、全部開く
            # listにattach
    return []


def __solve_by_double(board):
    # 隣り合う数字同士の差分と同じだけどちらかだけに隣接する未開放のセルがあれば、そこは確定する
    return []


def __guess(board):
    # 確率が一番少ないやつ適当にチョイス、あるいは0がなければ完全ランダムに。
    return [{"type": Const.CellAction.OPEN,
             "coord": [random.randrange(len(board)), random.randrange(len(board[0]))]}]
