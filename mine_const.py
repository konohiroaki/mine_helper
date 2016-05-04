class Const:
    class Padding:
        """
        Client Frame size.
        """
        LEFT = 12
        TOP = 55
        RIGHT = 12
        BOTTOM = 12

    class CellSize:
        WIDTH = 16
        HEIGHT = 16

    class BoardStatus:
        START = 0
        MIDSTREAM = 1
        END = 2
        BURST = 3

    class Cell:
        ZERO = (0, "  ")
        ONE = (1, " 1")
        TWO = (2, " 2")
        THREE = (3, " 3")
        FOUR = (4, " 4")
        FIVE = (5, " 5")
        SIX = (6, " 6")
        SEVEN = (7, " 7")
        EIGHT = (8, " 8")

        CLOSED = (10, " -")
        FLAGGED = (11, " F")
        QUESTION = (12, " Q")

        MINE = (20, " *")
        BURST = (21, " !")
        WRONG_FLAG = (22, " X")

    class Color:
        """
        Needs three pixels to distinguish a cell. But some only needs two. Burst only needs one.
        """
        POSITION = ({"Y": 1, "X": 1}, {"Y": 3, "X": 9}, {"Y": 6, "X": 6})

        ZERO = ((192, 192, 192), (192, 192, 192), (192, 192, 192))
        ONE = (ZERO[0], (0, 0, 255))
        TWO = (ZERO[0], (0, 128, 0))
        THREE = (ZERO[0], (255, 0, 0))
        FOUR = (ZERO[0], (0, 0, 128))
        FIVE = (ZERO[0], (128, 0, 0))
        SIX = (ZERO[0], (0, 128, 128))
        SEVEN = (ZERO[0], (0, 0, 0))
        EIGHT = (ZERO[0], (128, 128, 128))

        CLOSED = ((255, 255, 255), (192, 192, 192), (192, 192, 192))
        FLAGGED = (CLOSED[0], CLOSED[1], (255, 0, 0))
        QUESTION = (CLOSED[0], (0, 0, 0))

        MINE = (ZERO[0], ZERO[1], (255, 255, 255))
        BURST = (255, 0, 0)
        WRONG_FLAG = (ZERO[0], ZERO[1], (255, 0, 0))

    class CellAction:
        OPEN = 0
        FLAG = 1
