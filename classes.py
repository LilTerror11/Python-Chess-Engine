from copy import copy
from collections.abc import Sequence, Callable
from typing import Iterable, Any, Protocol, runtime_checkable, Optional
from warnings import warn

import pygame.mouse
from pygame import Vector2, Surface, Vector3
from builtins import print as log


# ------- HEHE --------

def print(*values, sep=" ", end="\n"):
    log("Classes: " + sep.join(str(v) for v in values), end=end)


# ------- ERRORS -------


# This means that there is no board asigned yet
class NoBoardException(Exception):
    ...


# This means that there
class UnknownPieceException(Exception):
    ...


class ConfigException(Exception):
    ...


class ConfigWarning(UserWarning):
    ...


class ConfigLoggingWarning(UserWarning):
    ...


# ------------ TYPES / CLASSES / FUNCTIONS ------------

coordinate = Vector2 | Sequence[int]
moves_format = list[list[int, int, int]] | list[tuple[int, int, int]]
takes_format = list[list[int, int, int]] | list[tuple[int, int, int]]


def flip_coordinate(pos: coordinate):
    """
    this is the fix for certain behind the scenes functions to make the (0,0) coordinate be the bottom left corner
    """
    pos = copy(pos)
    pos[1] = 7 - pos[1]
    return pos


def flip_y(y: int):
    """
    This is a 1 dimensional version of "flip_coordinate",
    See "flip_coordinate" for more info
    """
    return 7 - y


class GLOBAL:
    """

    """
    __events: dict
    __assets: dict
    __config_raw: dict

    @staticmethod
    def set_events(val):
        GLOBAL.__events = copy(val)

    @staticmethod
    def set_assets(val):
        GLOBAL.__assets = copy(val)

    @staticmethod
    def set_raw_config(val):
        GLOBAL.__config_raw = copy(val)

    @staticmethod
    def get_events():
        return GLOBAL.__events

    @staticmethod
    def get_assets():
        return GLOBAL.__assets

    @staticmethod
    def get_raw_config():
        return GLOBAL.__config_raw


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


class SharedList(list):
    ...


class Vector2Int:
    def __init__(self, x: int | float | Sequence[int | float], y: Optional[int | float] = None):
        if not isinstance(x, (int, float)):
            pos = [int(x[0]), int(x[1])]
        else:
            pos = [int(x), int(y)]

        self.__x = pos[0]
        self.__y = pos[1]

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    def __add__(self, other):
        other: Vector2 | Vector2Int
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other: Vector2 | Vector2Int
        return Vector2Int(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        other: Vector2 | Vector2Int | int | float

        if isinstance(other, int):
            return Vector2Int(self.__x * other, self.__y * other)

        if isinstance(other, float):
            return Vector2(self.__x * other, self.__y * other)

        if isinstance(other, Vector2Int):
            return Vector2Int(self.__x * other.x, self.__y * other.y)

        if isinstance(other, Vector2):
            return Vector2(self.__x * other.x, self.__y * other.y)

    def __truediv__(self, other):
        other: Vector2 | Vector2Int | int | float

        if isinstance(other, (float, int)):
            return Vector2(self.__x / other, self.__y / other)

        if isinstance(other, (Vector2, Vector2Int)):
            return Vector2(self.__x / other.x, self.__y / other.y)

    def __divmod__(self, other):
        other: Vector2 | Vector2Int | int | float

        if isinstance(other, (float, int)):
            dived = (divmod(self.__x, other), divmod(self.__x, other))
            return Vector2(dived[0][0], dived[1][0]), Vector2(dived[0][1], dived[1][1])

        if isinstance(other, (Vector2, Vector2Int)):
            dived = (divmod(self.__x, other.x), divmod(self.__x, other.y))
            return Vector2(dived[0][0], dived[1][0]), Vector2(dived[0][1], dived[1][1])

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __getitem__(self, item):
        if item == 0:
            return self.__x
        elif item == 1:
            return self.__y
        else:
            raise IndexError(item)

    def __setitem__(self, item, value):
        if item == 0:
            self.__x = value
        elif item == 1:
            self.__y = value
        else:
            raise IndexError(item)


class Mouse:
    def __init__(self, pos: coordinate, index: coordinate, pressed: tuple[bool, bool, bool] | list[bool, bool, bool]):
        self.__pos = pos
        self.__index = index
        self.__pressed = pressed

    def get_index(self):
        return Vector2Int(self.__index)

    def get_pos(self):
        return Vector2Int(self.__pos)

    def get_left_click(self):
        return self.__pressed[0]

    def get_middle_click(self):
        return self.__pressed[1]

    def get_right_click(self):
        return self.__pressed[2]

    def get_pressed(self):
        return self.__pressed


# "move"
# "take"
# "setup"
# "select"
# "tile_move"
# "tile_take"
# "on_move"
# "on_take"
# "on_event"

class IndexedEvent:
    key: str
    function: Callable

    def get_function(self):
        # print(GLOBAL.get_events())
        self.function = GLOBAL.get_events()[self.key]
        return self.function

    def __init__(self, val: str):
        self.key = val
        self.get_function()

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return self.key


class PieceEvents:
    def __init__(self, move="default.move", take="default.take", setup="default.null", select="default.null",
                 tile_move="default.tile_move", tile_take="default.tile_take", on_attack="default.null",
                 on_move="default.null", on_taken="default.null", on_event="default.null"):

        def to_list(val: list | Any):
            if isinstance(val, list):
                return val
            return [val]

        self.move = to_list(move)
        self.take = to_list(take)
        self.setup = to_list(setup)
        self.select = to_list(select)

        self.tile_move = to_list(tile_move)
        self.tile_take = to_list(tile_take)

        self.on_move = to_list(on_move)
        self.on_taken = to_list(on_taken)
        self.on_attack = to_list(on_attack)
        self.on_event = to_list(on_event)

        self.get_functions()

    def get_functions(self):
        def convert(val):
            for i in range(len(val)):
                val[i] = IndexedEvent(str(val[i]))

        convert(self.move)
        convert(self.take)
        convert(self.setup)
        convert(self.select)

        convert(self.tile_move)
        convert(self.tile_take)

        convert(self.on_move)
        convert(self.on_taken)
        convert(self.on_attack)
        convert(self.on_event)


@runtime_checkable
class HasMoveData(Protocol):
    def get_move_data(self) -> Any:
        ...


class GeneratedPiece:
    name: Optional[str] = None
    blank: Optional[bool] = None

    moves: Optional[list[list[int, int, int]]] = None
    takes: Optional[list[list[int, int, int]]] = None

    events: Optional[PieceEvents] = None

    display: Optional[AttributeDict[str, str | Surface]] = None

    piece_id: str

    __pieces = {}
    __piece_ids = []

    def __init__(self, config: AttributeDict | dict, piece_id: str):
        if isinstance(config, dict):
            config = AttributeDict(config)

        keys = list(config.keys())
        # print(piece_id)
        GeneratedPiece.__piece_ids.append(piece_id)
        self.piece_id = piece_id
        self.keys = keys

        self.blank = False

        if len(keys) == 0:
            warn(f"Piece \"id{piece_id}\" has no Config", ConfigWarning, stacklevel=3)
            warn(f"Piece \"id{piece_id}\" has been blanked", ConfigLoggingWarning, stacklevel=3)
            self.blank = True

        if keys.__contains__("blank"):
            self.blank = config.blank
        if not self.blank:
            # print(piece_id)
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
                icon_config = AttributeDict(config.icon["display"])
                if icon_config.type == "text":
                    if isinstance(icon_config.value, dict):
                        self.display = AttributeDict(icon_config.value)
                    elif isinstance(icon_config.value, str):
                        self.display = AttributeDict({"black": icon_config.value, "white": icon_config.value})
                elif icon_config.type == "image":
                    self.display = AttributeDict(icon_config.value)
            else:
                warn(f"Piece \"{self.name}\" is missing the \"icon\" tag", ConfigWarning, stacklevel=3)
                warn(f"Piece \"{self.name}\" has had its display be generated ({self.name[0].upper()})",
                     ConfigLoggingWarning, stacklevel=3)
                self.display = AttributeDict({"black": self.name.upper()[0], "white": self.name.upper()[0]})
            if keys.__contains__("events"):
                self.events = PieceEvents(**config.events)
            else:
                warn("Default piece events made", ConfigLoggingWarning, stacklevel=3)
                self.events = PieceEvents()
        GeneratedPiece.__pieces[piece_id] = self

    def generate_piece(self, colour: str = "null", pos: coordinate = Vector2(), board: Any = None):

        display = self.display
        piece = Piece(self.blank, self.events, self.moves, self.takes, display, self.name, self.piece_id, Vector2(pos),
                      colour, board)

        return piece

    @staticmethod
    def get_pieces():
        return copy(GeneratedPiece.__pieces)

    @staticmethod
    def get_piece_ids():
        return copy(GeneratedPiece.__piece_ids)


class Piece:
    """
    *"Active" Piece class*

    (Saying active here is just a fancy way to say it's a piece that has been generated and can do things)

    the Piece class is the basis for all pieces other than blank pieces
    it manages the events ran for the piece, generates moves

    ------

    Pieces are generated from a *GeneratedPiece* class, which is a scafold for a piece, it contains the event keys, the asset keys, and the raw moves for a piece

    **Functions**

    move(pos: coordinate) -> None
    ---
    Moves the piece to *pos*

    get_moves() -> SharedList[TileMoveEvent]
    ---
    Gets the pieces moves (generated from events)

    Note: a shared list functions exactly like a normal python list,
    although it has 1 slight change, it won't affect interacting with it

    get_moves() -> SharedList[TileTakeEvent]
    ---
    Gets the pieces takes (generated from events)

    Note: from looking at the code, they actually return a RawTileEvent (base for TileTakeEvent and TileMoveEvent),
    Eventually I might fix it so it returns the take / move specific ones, but :P there must be a reason

    ------

    **Variables**

    pos (Vector2)
    ---
    The pieces position

    piece_id (str)
    ---
    The pieces piece id (the id used in the board config setup)

    name (str)
    ---
    The pieces name (defined in config)

    display (it's either a image or a string, or something, can't be bothered figureing it out)
    ---
    The display (text or a image) (it's ALSO defined in config)

    events (PieceEvents)
    ---
    The events of the piece (ALSO defined in config)

    moves (moves_format)
    ---
    This is just the base of the moves, this is what is the simplistic move defined in config is used for

    takes (takes_format)
    ---
    Same as moves, but for takes

    move_count (int)
    ---
    The amount of moves this piece has made

    data (dict)
    ---
    Basically an attribute for adding "tags",
    and in a way so that you can check the tags it has and their values

    colour (str)
    ---
    is it black? or is it white? or is it, who knows!

    """

    pos: Vector2
    piece_id: str
    name: str
    display: dict[str, dict[str, Surface | str] | str]
    events: PieceEvents

    moves: moves_format
    takes: takes_format

    move_count: int = 0

    data: dict

    colour: str

    def __init__(self, blank: bool = False, events: Optional[PieceEvents] = None, moves: Optional[moves_format] = None,
                 takes: Optional[takes_format] = None,
                 display: Optional[dict[str, dict[str, Surface | str] | str]] = None, name: Optional[str] = None,
                 piece_id: Optional[str] = None, pos: Optional[coordinate | None] = Vector2(),
                 colour: Optional[str] = None, board: Any = None):
        self.blank = blank

        self.events = events
        self.moves = moves
        self.takes = takes

        self.move_count = 0

        self.display = display
        self.name = name
        self.piece_id = piece_id
        self.pos = pos

        self.colour = colour

        self.__board: Board = board

    def move(self, pos: int | coordinate, y: Optional[int] = None):
        if isinstance(pos, int):
            pos = Vector2(pos, y)
        self.move_count += 1
        self.__board.move(self.pos, pos)

    def get_moves(self):
        moves = []
        for move in self.moves:
            count = 0
            out = True
            pre_pos = copy(self.pos)
            moves_ = SharedList()
            while count < 64 and out:
                count += 1
                pos = pre_pos + Vector3(move).xy
                if not (0 <= int(pos.x) < 8) or not (0 <= int(pos.y) < 8):
                    break
                event_data = RawTileEvent(self, self.__board, move, self.pos, pos, pre_pos, count, moves_)
                for event in self.events.tile_move:
                    out = event(event_data)
                    pre_pos = event_data.pos
                    if not out:
                        break
            moves.append(list(moves_))
        event_data = MoveEvent(self, self.__board, self.pos, moves, self.moves)
        for event in self.events.move:
            event(event_data)
        return event_data.moves

    def get_takes(self):
        takes = []
        for take in self.takes:
            count = 0
            out = True
            pre_pos = copy(self.pos)
            takes_ = SharedList()
            while count < 64 and out:
                count += 1
                pos = pre_pos + Vector3(take).xy
                if not (0 <= int(pos.x) < 8) or not (0 <= int(pos.y) < 8):
                    break
                event_data = RawTileEvent(self, self.__board, take, self.pos, pos, pre_pos, count, takes_)
                for event in self.events.tile_take:
                    out = event(event_data)
                    pre_pos = event_data.pos
                    if not out:
                        break

            takes.append(list(takes_))
        event_data = TakeEvent(self, self.__board, self.pos, takes, self.takes)
        for event in self.events.take:
            event(event_data)
        return event_data.takes


# Board Class, this is the basis of the game, containing the pieces
# and helper functions used to move pieces around
class Board:
    """
    Board Class

    This class is used for most things, it contains the board
    """

    __board: list[list[Piece]] = []
    for x in range(8):
        __board.append([])
    board_init: list[list[int]]
    __assets: dict = None
    __events: dict = None

    __mouse: Mouse

    # Converts the config board into actual pieces, which have been generated as "GeneratedPiece"
    def gen_board(self):
        self.board_init: list[list[int]]

        # Columns
        for y in range(len(self.board_init)):
            row = self.board_init[flip_y(y)]
            # Rows
            for x in range(len(row)):
                # Pieces
                piece = row[x]
                # setting up the colour
                colour = "white"
                if piece < 0:
                    # if the piece is negative, then it means it's black
                    colour = "black"
                # If the piece isn't in config, raise an error
                if not GeneratedPiece.get_piece_ids().__contains__(str(abs(piece))):
                    raise UnknownPieceException(f"There is no piece of id \"id{abs(piece)}\"")
                # Get the piece if it does exist
                generated_piece: GeneratedPiece = GeneratedPiece.get_pieces()[str(abs(piece))]
                # Generate the piece, filling out values like it's position, it's colour, and it's parent board
                piece_object = generated_piece.generate_piece(colour, (x, y), self)
                # Put the piece on the board
                self.__board[y].append(piece_object)

    def __init__(self, board: list[list[int]] = None):
        # Simple Board Setup stuff
        if board is None:
            # The config version of the board
            board = [[0] * 8] * 8
        self.board_init = board
        self.gen_board()

    def get_piece_at(self, x: coordinate | int, y: Optional[int] = None) -> Piece:
        """

        :param x: The y Position of the piece be got
        :param y: The x Position of the piece be got
        :return: Piece at (x, y)
        """
        if y is None:
            x: coordinate
            pos = Vector2(x)
            return self.__board[int(pos.y)][int(pos.x)]
        else:
            return self.__board[y][x]

    def spawn_piece(self, piece: int | GeneratedPiece, x: int | coordinate, y: Optional[int] = None):

        """
        :param piece: A GeneratedPiece, or a piece index (int)
        :param x: The x position of the piece.
        :param y: The y position of the piece.
        :return: The piece being generated.
        """

        if y is None:
            x, y = x

        colour = "white"

        if piece < 0:
            colour = "black"

        if not isinstance(piece, GeneratedPiece):
            generated_piece: GeneratedPiece = GeneratedPiece.get_pieces()[str(piece)]
        else:
            generated_piece = piece

        piece = generated_piece.generate_piece(colour, (x, y), self)

        # print(piece.piece_id)

        self.__board[flip_y(y)][x] = piece

        return piece

    def move(self, pos1: coordinate, pos2: coordinate, replace: GeneratedPiece | int = 0):
        """

        :param pos1: The position of the piece getting moved
        :param pos2: The new position
        :param replace: [Optional] the piece getting left behind after the move
        :return: None
        """

        pos1_ = flip_coordinate(pos1)
        pos2_ = flip_coordinate(pos2)

        self.__board[int(pos2_[1])][int(pos2_[0])] = copy(self.__board[int(pos1_[1])][int(pos1_[0])])
        self.spawn_piece(replace, pos1)

    def get_board(self):
        """
        :return: A Copy of the board (cannot be used to change the raw board)
        """
        return copy(self.__board)

    @staticmethod
    def attach_events(events):
        Board.__events = events

    @staticmethod
    def get_events():
        return copy(Board.__assets)

    @staticmethod
    def attach_assets(assets):
        Board.__assets = assets

    @staticmethod
    def get_assets():
        return copy(Board.__assets)

    def __str__(self):
        # print(" a ".join(str(len(self.__board[x])) for x in range(len(self.__board))))
        return "[ " + " ],\n[ ".join(
            ", ".join(r.piece_id for r in self.__board[i]) for i in range(len(self.__board))) + " ]"

    def attach_mouse(self, mouse):
        self.__mouse = mouse

    def get_mouse(self):
        return self.__mouse


# ------- EVENTS -------

# Base Event class, for global values in events
class Event:
    """
    This is the basis for events
    Contains global event attributes (Things every event has)
    """
    __board: Board = None
    piece: Piece

    @staticmethod
    def set_board(board: Board):
        """
        :param board: You don't need to know this :P
        :return: None
        """
        Event.__board = board

    @staticmethod
    def get_board():
        """
        :return: The ***board***
        """
        if Event.__board:
            return Event.__board
        else:
            raise NoBoardException("No Board has been set")

    def get_piece(self):
        return self.piece


class RawTileEvent(Event):
    """
    """
    piece: Piece
    __raw_move: list[int, int, int]
    start: coordinate
    pos: coordinate
    pre: coordinate
    count: int
    moves: SharedList

    func: Callable = lambda *x: ...

    __length: int = 0
    board: Board

    def __init__(self,
                 piece: Piece,
                 board: Board,
                 raw_data: list[int, int, int],
                 start: coordinate,
                 pos: coordinate,
                 pre: coordinate,
                 count: int,
                 moves: SharedList
                 ):
        self.piece = piece
        self.raw_data = raw_data
        self.start = start
        self.pre = pre
        self.pos = pos
        self.board = board
        self.count = count
        self.moves = moves
        self.__canceled = False
        self.type = self.__class__

        self.moves.append(self)

    def __len__(self):
        """
        :return: The amount of children on this event
        """
        return self.__length

    def __repr__(self):
        return "{" + f'type:"{self.type}", piece:{self.piece}, raw_data:{self.raw_data}, start:{self.start}, pre:{self.pre}, pos:{self.pos}, count:{self.count}' + "}"

    def __str__(self):
        return "{" + f'type:"{self.type}", piece:{self.piece}, raw_data:{self.raw_data}, start:{self.start}, pre:{self.pre}, pos:{self.pos}, count:{self.count}, moves:{self.moves}' + "}"

    def __iter__(self):
        return self.moves

    def attach_function(self, func: Callable):
        self.func = func

    def cancel(self, val: bool = False):
        self.__canceled = True
        return val

    def is_canceled(self):
        return self.__canceled

    def get_next(self):
        if len(self.moves) >= self.count + 1:
            return None
        return self.moves[self.count + 1]

    def get_previous(self):
        if self.count - 1 > 0:
            return self.moves[self.count - 1]
        return None


class TileTakeEvent(RawTileEvent):
    ...


class TileMoveEvent(RawTileEvent):
    ...


# I have no clue what this is for
# (THIS IS WHY YOU COMMENT YOUR CODE!!!!)
class MoveData(Event):
    pos: Vector2
    piece: Piece
    move: list[int, int, int]

    def __init__(self, piece: Piece | HasMoveData, move: Optional[list[int, int, int]] = None,
                 x: int | coordinate = None, y: Optional[int] = None):
        if isinstance(piece, HasMoveData):
            move_data: MoveData = piece.get_move_data()
            self.pos = copy(move_data.pos)
        else:
            if y is None:
                self.pos = Vector2(x)
            else:
                self.pos = Vector2(x, y)
            self.move = move

    def get_move_data(self):
        return self


class MoveEvent(Event):
    piece: Piece
    moves: list[list[TileMoveEvent]]
    raw_moves: list[list[int, int, int]]

    def __init__(self, piece: Piece, board: Board, pos, moves, raw_moves):
        self.piece = piece
        self.moves = moves
        self.pos = pos
        self.raw_moves = raw_moves


class TakeEvent(Event):
    piece: Piece
    moves: list[list[TileTakeEvent]]
    raw_takes: list[list[int, int, int]]

    def __init__(self, piece: Piece, board: Board, pos: coordinate, takes, raw_takes):
        self.piece = piece
        self.takes = takes
        self.takes: list
        self.takes.insert(0, [])
        self.pos: Sequence[int] = pos
        self.raw_takes = raw_takes

    def add_take(self, pos: coordinate, function: Optional[callable] | str = None):
        raw: list[int] = [pos[0] - self.pos[0], pos[1] - self.pos[1], 1]
        raw: list[int, int, int]
        event = RawTileEvent(
            piece=self.piece,
            board=self.get_board(),
            raw_data=raw,
            start=self.pos,
            pos=pos,
            pre=self.pos,
            count=0,
            moves=SharedList(),
        )

        if function:
            if type(function) is str:
                function = IndexedEvent(function)
            event.attach_function(function)

        self.takes[0].append(event)
        return event
