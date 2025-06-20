from typing import Optional # noqa

from classes import MoveEvent, TakeEvent, TileTakeEvent, TileMoveEvent, RawTileEvent
from pygame import Vector2, Vector3 # noqa


def default_tile_blocked(event: RawTileEvent):
    piece = event.get_board().get_piece_at(event.pos)
    if piece.piece_id != "0":
        return False
    return True


def default_tile_move(event: TileMoveEvent):
    """
    This is the default function for TileMoveEvent
    To prevent the move from showing, cancel the event with 'event.cancel()'
    returning False ends the iteration on this path of events
    """
    if not default_tile_blocked(event):
        return event.cancel()

    if event.count >= event.raw_data[2]:
        return False
    else:
        return True


def default_tile_take(event: TileTakeEvent):
    """
    This is the default function for TileTakeEvent
    To prevent the move from showing, cancel the event with 'event.cancel()'
    returning False ends the iteration on this path of events
    """
    if not default_tile_blocked(event):
        if event.get_board().get_piece_at(event.pos).colour == event.get_piece().colour:
            event.cancel()
        return False

    event.cancel()

    if event.count > event.raw_data[2]:
        return False
    else:
        piece = event.get_piece()
        return piece.colour == event.get_board().get_piece_at(event.pos).colour


def default_directional_tile_move(event: TileMoveEvent):
    """
    This function just inverts the move if the piece is a "black" piece
    This function will overwrite the default tile move function
    """
    piece = event.get_piece()
    if piece.colour == "black":
        event.pos = event.pre - Vector3(event.raw_data).xy
        print(event.pos, event.pre)
    return True


def default_directional_tile_take(event: TileTakeEvent):
    """
    This function just inverts the takes if the piece is a "black" piece
    This function will overwrite the default tile take function
    """
    piece = event.get_piece()
    if piece.colour == "black":
        event.pos = event.pre - Vector3(event.raw_data).xy
    return True


def default_move(event: MoveEvent):
    """
    Placeholder function that has no effect
    """
    return event


def default_take(event: TakeEvent):
    """
    Placeholder function that has no effect
    """
    return event

