from classes import TileMoveEvent
from defaults import default_move, default_take, default_tile_move, default_tile_take, default_directional_tile_move, default_directional_tile_take

from defaults import default_tile_blocked

# Leave this, it makes adding events much easier
def def_event(name):
    global events
    return lambda func: func if events.__setitem__(name, func) else func

events = {
    "default.null": lambda *x: ...,
    "default.move": default_move,
    "default.take": default_take,
    "default.tile_move": default_tile_move,
    "default.tile_take": default_tile_take,
    "default.direction_tile_move": default_directional_tile_move,
    "default.direction_tile_take": default_directional_tile_take
}

# Example Events
@def_event("pawn.tile_move")
def pawn_tile_move(event: TileMoveEvent):
    if not default_tile_blocked(event):
        return event.cancel()

    piece = event.get_piece()

    count = event.count - int(piece.moves == 0)
    if count <= event.raw_data[2]:
        return True
    return False
