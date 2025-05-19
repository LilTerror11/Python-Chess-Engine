from classes import MoveEvent, TileMoveEvent


def default_tile_move(event: TileMoveEvent):
    if event.get_board().get_piece_at(event.pos):
        ...
    if event.count > event.raw_move[2]:
        return False, event
    else:
        return True, event


def default_move(event: MoveEvent):
    ...

