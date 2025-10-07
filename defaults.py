from typing import Optional # noqa

from classes import MoveEvent, TakeEvent, TileTakeEvent, TileMoveEvent, RawTileEvent, RenderEvent, AttributeDict
from pygame import Vector2, Vector3, Surface # noqa
from pygame.transform import scale_by
from classes import GLOBAL

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
        return True


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
            #print(piece.display)
            #print(piece.piece_id)
            display = piece.display[piece.colour]
            piece_colour = piece_colour1, piece_colour2
            if piece.colour == "black":
                piece_colour = piece_colour2, piece_colour1
            if isinstance(display, Surface):
                image = scale_by(display.copy(), tile_size_ * 0.8 / max(display.get_size()))
                tile_surf.blit(image, Vector2(tile_size_ * 0.1))
            else:

                text_surf1 = scale_by(placeholder_font_bold.render(str(display), False,
                                                                   piece_colour[0]), tile_size_ / 100)
                text_surf2 = scale_by(placeholder_font_bold.render(str(display), False,
                                                                   piece_colour[1]), tile_size_ / 100)
                tile_surf.blit(text_surf2, Vector2(tile_size_) / 2 - Vector2(text_surf2.get_size()) / 2 - Vector2(0, 1))
                tile_surf.blit(text_surf2, Vector2(tile_size_) / 2 - Vector2(text_surf2.get_size()) / 2 - Vector2(1, 0))
                tile_surf.blit(text_surf2, Vector2(tile_size_) / 2 - Vector2(text_surf2.get_size()) / 2 + Vector2(0, 1))
                tile_surf.blit(text_surf2, Vector2(tile_size_) / 2 - Vector2(text_surf2.get_size()) / 2 + Vector2(1, 0))
                tile_surf.blit(text_surf1, Vector2(tile_size_) / 2 - Vector2(text_surf1.get_size()) / 2)

            tile_surf.fill(piece_colour[1],
                            (Vector2(0, 0.76) * tile_size_, Vector2(tile_size_ * 0.24)))
            tile_surf.fill(piece_colour[0],
                            (Vector2(0.02, 0.78) * tile_size_, Vector2(tile_size_ * 0.2)))


events = {
    # --- Built in events ---
    # Default events (these are used by default if no config for events is defined)
    "default.null": lambda *x: ...,
    "default.move": default_move,
    "default.take": default_take,
    "default.tile_move": default_tile_move,
    "default.tile_take": default_tile_take,
    "default.render": default_render,
    # Default helper events (these aren't used as any defaults, but they are nice helper events)
    "default.direction_tile_move": default_directional_tile_move,
    "default.direction_tile_take": default_directional_tile_take
}

GLOBAL.set_events(events)

print(events)
print(GLOBAL.get_events())
