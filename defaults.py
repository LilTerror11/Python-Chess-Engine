from typing import Optional # noqa

from classes import MoveEvent, TakeEvent, TileTakeEvent, TileMoveEvent, RawTileEvent, RenderEvent
from pygame import Vector2, Vector3, Surface # noqa
from pygame.transform import scale_by


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

    if event.count >= event.raw_data[2]:
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
        event.pos = event.pre + Vector2(event.raw_data[0], -event.raw_data[1])
    return True


def default_directional_tile_take(event: TileTakeEvent):
    """
    This function just inverts the takes if the piece is a "black" piece
    This function will overwrite the default tile take function
    """
    piece = event.get_piece()
    if piece.colour == "black":
        event.pos = event.pre + Vector2(event.raw_data[0], -event.raw_data[1])
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

def default_render(event: RenderEvent):

    piece = event.get_piece()
    tile_surf = event.get_surface()
    x, y = event.pos
    variables = event.get_variables()
    piece_colour1 = variables["piece_colour1"]
    piece_colour2 = variables["piece_colour2"]

    board_colour = variables["board_colour"]

    placeholder_font_bold = variables["placeholder_font_bold"]

    tile_size_ = event.tile_size

    if not piece.blank:
        if piece.colour != "null":
            display = piece.display[piece.colour]
            piece_colour = piece_colour1, piece_colour2
            if piece.colour == "black":
                piece_colour = piece_colour2, piece_colour1
            if isinstance(display, Surface):
                ...
            else:

                text_surf1 = scale_by(placeholder_font_bold.render(str(display), False,
                                                                   board_colour[1]), tile_size_ / 100)
                tile_surf.blit(text_surf1, Vector2(tile_size_) / 2 - Vector2(text_surf1.get_size()) / 2)

                tile_surf.fill(piece_colour[1],
                                (Vector2(0, 0.76) * tile_size_, Vector2(tile_size_ * 0.24)))
                tile_surf.fill(piece_colour[0],
                                (Vector2(0.02, 0.78) * tile_size_, Vector2(tile_size_ * 0.2)))
