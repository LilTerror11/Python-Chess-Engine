from typing import Any
from typing import Iterable


class Piece:
    def __init__(self):
        ...


class Board:

    __board: list[list[Piece]] = [[None] * 8] * 8
    board_init: list[list[int]]

    def gen_board(self):
        self.board_init: list[list[int]]
        for x in range(len(self.board_init)):
            row = self.board_init[x]
            for y in range(len(row)):
                piece = row[y]
                self.__board[x][y] = Piece()

    def __init__(self, board: list[list[int]]=None):
        if board is None:
            board = [[0] * 8] * 8
        self.board_init = board
        self.gen_board()

    def get_piece_at(self, x, y) -> Piece:
        return self.__board[x][y]


class AttributeDict(dict):
    """
    Unused so far
    """
    def __init__(self, val: Any = None):
        def update(__):
            for _ in __:
                if isinstance(_, dict):
                    update(_)
                else:
                    __[_] = __[_]

        if isinstance(val, Iterable):
            super().__init__(val)
            update(self)
        else:
            super().__init__()

    def __setitem__(self, key, value):
        super().__setattr__(key, value)
        print(self)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)


# ------- EVENTS -------

class TileMoveEvent:

    piece: Piece
    raw_move: list[int, int, int]
    start: list[int, int]
    pos: list[int, int]
    count: int
    child: Any | None
    parent: Any | None

    __length: int = 0


    def __init__(self,
                 piece: Piece,
                 raw_move: list[int, int, int],
                 start: list[int, int],
                 pos: list[int, int],
                 count: int,
                 parent = None
                 ):
        self.piece = piece
        self.raw_move = raw_move
        self.start = start
        self.pos = pos
        self.count = count
        self.parent = parent
        self.child = None
        self.type = self.__class__
        if isinstance(parent, TileMoveEvent):
            parent.child = self
            self.__length = parent.__length + 1

    def __len__(self):
        """
        :return: The amount of children on this event
        """
        return self.__length

    def __repr__(self):
        return "{" + f'type:"{self.type}", piece:{self.piece}, raw_move:{self.raw_move}, start:{self.start}, pos:{self.pos}, count:{self.count}, parent:{True if self.parent else False}, child:{True if self.child else False}' + "}"

    def get_child(self):
        if self.child:
            return self.child
        else:
            return None

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return None

    def __iter__(self):
        if self.parent:
            return iter([self, *list(self.parent)])
        return iter([self])


class TileTakeEvent:

    piece: Piece
    raw_take: list[int, int, int]
    start: list[int, int]
    pos: list[int, int]
    count: int
    child: Any | None
    parent: Any | None

    __length: int = 0

    def __init__(self,
                 piece: Piece,
                 raw_take: list[int, int, int],
                 start: list[int, int],
                 pos: list[int, int],
                 count: int,
                 parent = None
                 ):
        self.piece = piece
        self.raw_take = raw_take
        self.start = start
        self.pos = pos
        self.count = count
        self.parent = parent
        self.child = None
        self.type = self.__class__
        if isinstance(parent, TileTakeEvent):
            parent.child = self
            self.__length = parent.__length + 1

    def __len__(self):
        """
        :return: The amount of children on this event
        """
        return self.__length

    def __repr__(self):
        return "{" + f'type:"{self.type}", piece:{self.piece}, raw_move:{self.raw_take}, start:{self.start}, pos:{self.pos}, count:{self.count}, parent:{True if self.parent else False}, child:{True if self.child else False}' + "}"

    def get_child(self):
        if self.child:
            return self.child
        else:
            return None

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return None

    def __iter__(self):
        if self.parent:
            return iter([self, *list(self.parent)])
        return iter([self])


class MoveEvent:
    piece: Piece
    moves: list[TileMoveEvent]
    raw_moves: list[list[int, int, int]]

    def __init__(self, piece, moves, raw_moves):
        self.piece = piece
        self.moves = moves
        self.raw_moves = raw_moves


class TakeEvent:
    piece: Piece
    moves: list[TileTakeEvent]
    raw_takes: list[list[int, int, int]]

    def __init__(self, piece, moves, raw_takes):
        self.piece = piece
        self.moves = moves
        self.raw_takes = raw_takes
