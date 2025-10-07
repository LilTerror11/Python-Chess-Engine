from pygame import Vector2, Surface
from pygame.transform import scale_by, scale # noqa

from classes import TileMoveEvent, MoveEvent, OnAttackEvent, GeneratedPiece, RenderEvent, TakeEvent, GLOBAL, \
    AttributeDict
from defaults import default_move, default_take, default_tile_move, default_tile_take, \
    default_directional_tile_move, default_directional_tile_take, default_render

from defaults import default_tile_blocked
# from defaults import events


# Leave this, it makes adding events much easier
def def_event(name):
    #global events
    return lambda func: func if GLOBAL.get_events().__setitem__(name, func) else func

# This is a helper function to make making new pieces from this file easier
# In order to define a piece in functions, the events have to already be defined, there is no way around this
# Otherwise the program breaks, and errors out, another thing is that the events have to be set (kina makes sense)
def define_piece(config, piece_id):
    #GLOBAL.set_events(events)
    GeneratedPiece(config, piece_id)


# Events
{ # noqa
    # --- Built in events ---
    # Default events (these are used by default if no config for events is defined)
    "default.null": lambda *x: ...,
    "default.move": default_move,
    "default.take": default_take,
    "default.tile_move": default_tile_move,
    "default.tile_take": default_tile_take,
    # This is the render event for each tile
    "default.render": default_render,
    # Default helper events (these aren't used as any defaults, but they are nice helper events)
    "default.direction_tile_move": default_directional_tile_move,
    "default.direction_tile_take": default_directional_tile_take
}


# Example Events
@def_event("pawn.tile_move")
def pawn_tile_move(event: TileMoveEvent):
    if not default_tile_blocked(event):
        return event.cancel()

    piece = event.get_piece()

    count = event.count - int(piece.move_count == 0)
    if count < event.raw_data[2]:
        return True
    return False

print(GLOBAL.get_events()["pawn.tile_move"])


@def_event("custom.tile_move_through")
def custom_tile_move_through(event: TileMoveEvent):
    if not default_tile_blocked(event):
        return event.cancel(True)

    if event.count <= event.raw_data[2]:
        return True
    return False


def double_move(*args, **kwargs):
    print(args, kwargs)


@def_event("pawn.move")
def pawn_move(event: MoveEvent):
    event.add_move((event.get_piece().pos + Vector2(0, [-1, 1][int(event.get_piece().colour == "black")])))


@def_event("absorb.attack")
def gain_attack(event: OnAttackEvent):
    piece = event.get_piece()
    target = event.get_target()
    moves = GeneratedPiece.get_pieces()[target.piece_id].moves
    print(moves)
    if not piece.data.keys().__contains__("gained"):
        piece.data["gained"] = set()

    if target.piece_id != piece.piece_id:
        piece.data["gained"].add(target.piece_id)
        print(piece.data["gained"])

    #for move in moves:
    #    if move not in piece.moves:
    #        piece.moves.append(move)


@def_event("absorb.move")
def gain_move(event: MoveEvent):
    piece = event.get_piece()
    if "gained" in piece.data.keys():
        for x in piece.data["gained"]:
            gened = GeneratedPiece.get_pieces()[x].generate_piece(piece.colour, piece.pos, event.get_board())
            gened.move_count = piece.move_count
            moves = gened.get_moves()
            del gened
            for move in moves:
                if move not in event.moves:
                    event.moves.append(move)


@def_event("absorb.take")
def gain_take(event: TakeEvent):
    piece = event.get_piece()
    if "gained" in piece.data.keys():
        for x in piece.data["gained"]:
            gened = GeneratedPiece.get_pieces()[x].generate_piece(piece.colour, piece.pos, event.get_board())
            gened.move_count = piece.move_count
            takes = gened.get_takes()
            del gened
            for take in takes:
                if take not in event.takes:
                    event.takes.append(take)


@def_event("default.render")
def render_event(event: RenderEvent):
    default_render(event)
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
            piece_colour = piece_colour1, piece_colour2
            if piece.colour == "black":
                piece_colour = piece_colour2, piece_colour1
            if "gained" in piece.data.keys():
                c = 0
                for i in piece.data["gained"]:
                    piece2 = GeneratedPiece.get_pieces()[i]
                    if piece2.icon:
                        ...
                    else:
                        display = piece2.display[piece.colour]
                        text_surf1 = scale_by(placeholder_font_bold.render(str(display), False,
                                                                           board_colour[1]), (tile_size_ / 100) * 0.17)
                        tile_surf.blit(text_surf1, Vector2(0.83, 0.2 * c) * tile_size_)
                    c += 1

                #tile_surf.fill(piece_colour[1],
                #               (Vector2(0, 0.76) * tile_size_, Vector2(tile_size_ * 0.24)))
                #tile_surf.fill(piece_colour[0],
                #               (Vector2(0.02, 0.78) * tile_size_, Vector2(tile_size_ * 0.2)))


define_piece({
        "name": "absorber",
        "moves": [
            [0, 1, 1],
            [0, -1, 1],
            [1, 0, 1],
            [-1, 0, 1]
        ],
        "takes": [
            [1, 1, 1],
            [-1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1]
        ],
        "events": {
            "on_attack": "absorb.attack",
            "move": [
                "default.move",
                "absorb.move"
            ],
            "take": [
                "default.take",
                "absorb.take"
            ]
        },
        "icon": {
            "display": {
               "type": "text",
               "value": "@"
            }
        }
    }, "9")

