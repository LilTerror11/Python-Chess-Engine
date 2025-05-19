import copy
import warnings
from collections.abc import Callable, Sequence
from typing import Iterable, Any, Protocol, runtime_checkable, Optional
from warnings import warn

from pygame import Vector2, Surface

# ------- ERRORS -------


class NoBoardException(Exception):
    ...

class ConfigException(Exception):
    ...

class ConfigWarning(UserWarning):
    ...

class ConfigLoggingWarning(UserWarning):
    ...


# ------------ TYPES / CLASSES ------------

coordinate = Vector2 | Sequence[int]


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

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

# "move"
# "take"
# "setup"
# "select"
# "tile_move"
# "tile_take"
# "on_move"
# "on_take"
# "on_event"

class PieceEvents:
    def __init__(self, move = "default.move", take = "default.take", setup = "default.null",
                 tile_move = "default.tile_move", tile_take = "default.tile_take", on_attack = "default.null",
                 on_move = "default.null", on_taken = "default.null", on_event = "default.null"):

        def list_str(val: list | str):
            if isinstance(val, str):
                return [val]
            return val

        self.move = list_str(move)
        self.take = list_str(take)
        self.setup = list_str(setup)

        self.tile_move = list_str(tile_move)
        self.tile_take = list_str(tile_take)

        self.on_move = list_str(on_move)
        self.on_taken = list_str(on_taken)
        self.on_attack = list_str(on_attack)
        self.on_event = list_str(on_event)


@runtime_checkable
class HasMoveData(Protocol):
    def get_move_data(self) -> None:
        ...

class GeneratedPiece:
    name: Optional[str] = None
    blank: Optional[bool] = None

    moves: Optional[list[list[int, int, int]]] = None
    attack: Optional[list[list[int, int, int]]] = None

    events: Optional[AttributeDict[str]] = None

    display: Optional[AttributeDict[str, str | Surface]] = None

    __pieces = {}
    __piece_ids = {}

    def __init__(self, config: AttributeDict | dict, piece_id: str):
        if isinstance(config, dict):
            config = AttributeDict(config)

        keys = list(config.keys())
        self.keys = keys

        self.blank = False

        if len(keys) == 0:
            warn(f"Piece \"id{piece_id}\" has no Config", ConfigWarning, stacklevel=3)
            warn(f"Piece \"id{piece_id}\" has been blanked", ConfigLoggingWarning, stacklevel=3)
            self.blank = True

        if keys.__contains__("blank"):
            self.blank = config.blank
        if not self.blank:
            print(piece_id)
            if keys.__contains__("name"):
                self.name = config.name
            else:
                raise ConfigException(f"Non blank piece \"id{piece_id}\" doesn't have \"name\" tag")
            if keys.__contains__("moves"):
                self.moves = config.moves
            else:
                warn(f"Piece \"{self.name}\" is missing the \"moves\" tag", ConfigWarning, stacklevel=3)
                warn(f"Piece \"{self.name}\" has had its moves blanked", ConfigLoggingWarning, stacklevel=3)
                self.moves = []
            if keys.__contains__("takes"):
                self.takes = config.takes
            else:
                warn(f"Piece \"{self.name}\" is missing the \"takes\" tag", ConfigWarning, stacklevel=3)
                warn(f"Piece \"{self.name}\" has had its takes blanked", ConfigLoggingWarning, stacklevel=3)
                self.takes = []
            if keys.__contains__("icon"):
                icon_config = config.icon.display
                if icon_config.type == "text":
                    if isinstance(icon_config.value, dict):
                        self.display = AttributeDict(icon_config.value)
                    elif isinstance(icon_config.value, str):
                        self.display = AttributeDict({"black": icon_config.value, "white": icon_config.value})
                elif icon_config.type == "image":
                    self.display = AttributeDict(icon_config.value)
            else:
                warn(f"Piece \"{self.name}\" is missing the \"icon\" tag", ConfigWarning, stacklevel=3)
                warn(f"Piece \"{self.name}\" has had its display be generated ({self.name[0].upper()})", ConfigLoggingWarning, stacklevel=3)
                self.display = AttributeDict({"black": self.name.upper()[0], "white": self.name.upper()[0]})
        GeneratedPiece.__pieces[piece_id] = self

    def generate_piece(self, assets, events):
        ...

    @staticmethod
    def get_pieces():
        return copy.copy(GeneratedPiece.__pieces)

    @staticmethod
    def get_piece_ids():
        return copy.copy(GeneratedPiece.__piece_ids)


class Piece:
    def __init__(self, events, ):
        ...


class Board:

    __board: list[list[Piece]] = [[None] * 8] * 8
    board_init: list[list[int]]
    __assets: dict = None
    __events: dict = None

    def gen_board(self):
        self.board_init: list[list[int]]
        for x in range(len(self.board_init)):
            row = self.board_init[x]
            for y in range(len(row)):
                piece = row[y]
                self.__board[x][y] = None

    def __init__(self, board: list[list[int]]=None):
        if board is None:
            board = [[0] * 8] * 8
        self.board_init = board
        self.gen_board()

    def get_piece_at(self, x: coordinate | int, y: Optional[int] = None) -> Piece:
        if y:
            return self.__board[x][y]
        else:
            return self.__board[x[0]][x[1]]

    def spawn_piece(self, piece: str | GeneratedPiece, x: int | coordinate, y: Optional[int] = None):
        if y is None:
            x, y = x

        if not isinstance(piece, GeneratedPiece):
            generated_piece: GeneratedPiece = GeneratedPiece.get_pieces()[piece]
            generated_piece.generate_piece(self.__assets, self.__events)

    @staticmethod
    def attach_events(events):
        Board.__events = events

    @staticmethod
    def get_events():
        return copy.copy(Board.__assets)

    @staticmethod
    def attach_assets(assets):
        Board.__assets = assets

    @staticmethod
    def get_assets():
        return copy.copy(Board.__assets)


# ------- EVENTS -------

# Base Event class, for global values in events
class Event:
    __board: Board = None

    @staticmethod
    def set_board(board: Board):
        Event.__board = board

    @staticmethod
    def get_board():
        if Event.__board:
            return Event.__board
        else:
            raise NoBoardException("No Board has been set")


class TileMoveEvent(Event):

    piece: Piece
    raw_move: list[int, int, int]
    start: coordinate
    pos: coordinate
    pre: coordinate
    count: int
    child: Any | None
    parent: Any | None

    __length: int = 0
    board: Board


    def __init__(self,
                 piece: Piece,
                 board: Board,
                 raw_move: list[int, int, int],
                 start: coordinate,
                 pos: coordinate,
                 pre: coordinate,
                 count: int,
                 parent = None,
                 ):
        self.piece = piece
        self.raw_move = raw_move
        self.start = start
        self.pre = pre
        self.pos = pos
        self.board = board
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


class TileTakeEvent(Event):

    piece: Piece
    raw_take: list[int, int, int]
    start: coordinate
    pos: coordinate
    pre: coordinate
    count: int
    child: Any | None
    parent: Any | None
    board: Board

    __length: int = 0

    def __init__(self,
                 piece: Piece,
                 board: Board,
                 raw_take: list[int, int, int],
                 start: coordinate,
                 pre: coordinate,
                 pos: coordinate,
                 count: int,
                 parent = None,
                 ):
        self.board = board
        self.piece = piece
        self.raw_take = raw_take
        self.start = start
        self.pos = pos
        self.pre = pre
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


class MoveData(Event):
    pos: Vector2
    piece: Piece

    def __init__(self, piece: Piece | HasMoveData, x: int | coordinate  = None, y: Optional[int] = None):
        if isinstance(piece, HasMoveData):
            print(piece.get_move_data())
        elif isinstance(x, int):
            if y is None:
                self.pos = Vector2(x)
            else:
                self.pos = Vector2(x, y)

    def get_move_data(self):
        return self


class MoveEvent(Event):
    piece: Piece
    moves: list[TileMoveEvent]
    raw_moves: list[list[int, int, int]]

    def __init__(self, piece, moves, raw_moves):
        self.piece = piece
        self.moves = moves
        self.raw_moves = raw_moves


class TakeEvent(Event):
    piece: Piece
    moves: list[TileTakeEvent]
    raw_takes: list[list[int, int, int]]

    def __init__(self, piece, moves, raw_takes):
        self.piece = piece
        self.moves = moves
        self.raw_takes = raw_takes
