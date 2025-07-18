import sys
import time
from copy import copy

import pygame
import json

from pygame import Vector2, Vector3, Surface
from pygame.transform import scale_by

from classes import AttributeDict, Board, GeneratedPiece, GLOBAL, Event, flip_coordinate, flip_y, Mouse, \
    Vector2Int, SharedList, RenderEvent
from functions import events


print("Python Chess!")


debugging = False

for path in sys.path:
    if path.__contains__("\\python-ce\\helpers\\pydev"):
        print("Running in Intellij Debugger")
        break


def load_json(file_path) -> dict:
    with open(file_path) as file:
        data: dict = json.load(file)
    return data


def save_data(file_path, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2) # noqa

GLOBAL.set_events(events)

config = AttributeDict(load_json("config.json"))
GLOBAL.set_raw_config(config)

win = pygame.display.set_mode((600, 600), pygame.RESIZABLE)


board_colour2 = Vector3(51, 29, 4)
board_colour1 = Vector3(255) - board_colour2

piece_colour1 = Vector3(255)
piece_colour2 = Vector3()

mouse_tile = None

for piece_config_key in config.pieces:
    piece_config_key: str
    piece_config: AttributeDict = config.pieces[piece_config_key]
    GeneratedPiece(piece_config, piece_config_key)
    # print(GeneratedPiece(piece_config, piece_config_key))

board = Board(config.board)
Event.set_board(board)


# board.spawn_piece(3, 4, 4)

pygame.font.init()
placeholder_font = pygame.font.SysFont("Consolas", 100)
placeholder_font_bold = pygame.font.SysFont("Consolas", 105, True)


def render():
    global win, moves

    size = Vector2(win.get_size())
    min_size_ = min(size)

    board_surf = pygame.Surface((min_size_, min_size_))

    tile_size_ = min_size_ / 8

    board_list = board.get_board()
    tile_surf = Surface(Vector2(tile_size_))
    for i in range(len(board_list)):
        row = board_list[i]
        y = flip_y(i)
        for x in range(len(row)):
            piece_ = row[x]
            board_colour = board_colour1, board_colour2
            if ((x + y) % 2) == 0:
                board_colour = board_colour2, board_colour1
            #board_surf.fill(board_colour[0], (Vector2(x, y) * tile_size_, Vector2(tile_size_)))
            tile_surf.fill(board_colour[0])
            render_event = RenderEvent(piece_, board, Vector2Int(x, y), tile_surf, copy(tile_size_), {
                "piece_colour1": piece_colour1,
                "piece_colour2": piece_colour2,
                "board_colour1": board_colour1,
                "board_colour2": board_colour2,
                "board_colour": board_colour,
                "placeholder_font": placeholder_font,
                "placeholder_font_bold": placeholder_font_bold,
            })
            events["default.render"](render_event)
            #del render_event
            #if not piece.blank:
            #    if piece.colour != "null":
            #        display = piece.display[piece.colour]
            #        piece_colour = piece_colour1, piece_colour2
            #        if piece.colour == "black":
            #            piece_colour = piece_colour2, piece_colour1
            #        if isinstance(display, Surface):
            #            ...
            #        else:
            #
            #            text_surf1 = scale_by(placeholder_font_bold.render(str(display), False,
            #                                                               board_colour[1]), tile_size_ / 100)
            #            board_surf.blit(text_surf1, Vector2(x, y) * tile_size_ + Vector2(tile_size_) / 2 - Vector2(text_surf1.get_size()) / 2)
            #
            #            board_surf.fill(piece_colour[1],
            #                            (Vector2(x, (y + 0.76)) * tile_size_, Vector2(tile_size_ * 0.24)))
            #            board_surf.fill(piece_colour[0],
            #                            (Vector2(x + 0.02, y + 0.78) * tile_size_, Vector2(tile_size_ * 0.2)))
            board_surf.blit(tile_surf, Vector2(x, y) * tile_size_)
    for n in moves:
        n: SharedList
        for m in n:
            if not m.is_canceled():
                board_surf.fill((255, 0, 0), (Vector2(m.pos[0], flip_y(m.pos[1]))*tile_size_, Vector2(20)))
            #else:
            #    board_surf.fill((255, 127, 0), (Vector2(m.pos[0], flip_y(m.pos[1]))*tile_size_, Vector2(20)))

    for n in takes:
        n: SharedList
        for m in n:
            if not m.is_canceled():
                board_surf.fill((0, 255, 0), (Vector2(m.pos[0], flip_y(m.pos[1]))*tile_size_, Vector2(20)))
            #else:
            #    board_surf.fill((255, 255, 0), (Vector2(m.pos[0], flip_y(m.pos[1]))*tile_size_, Vector2(20)))


    return board_surf, size / 2 - Vector2(board_surf.get_size()) / 2


def int_vector(vec):
    vec2 = copy(vec)
    for i in range(len(vec2)):
        vec2[i] = int(vec2[i])

    return vec2


selected_pos = Vector2(0, 0)

#moves = board.get_piece_at(0, 0).get_moves()
#takes = board.get_piece_at(0, 0).get_takes()

moves = []
takes = []


clicked = False

# print(board)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # print(board)

    # x1, y1 = input("pos1: ").split(",")
    # pos1 = (int(x1), int(y1))

    # x2, y2 = input("pos2: ").split(",")
    # pos2 = (int(x2), int(y2))

    win_size = Vector2(win.get_size())

    mouse = Vector2(pygame.mouse.get_pos())
    mouse = Vector2(mouse.x, win_size.y - mouse.y)

    min_size = min(win_size)

    tile_size = min_size / 8

    board_corner = win_size / 2 - Vector2(min_size) / 2

    mouse_board_pos = mouse - board_corner

    in_range = False

    if max(mouse_board_pos) < min_size and min(mouse_board_pos) > 0:
        in_range = True
        buttons = pygame.mouse.get_pressed(3)

        mouse_tile = Vector2Int(mouse_board_pos / tile_size)
        # print("\r" + str(list(mouse_tile)), end="")

    board_display = render()

    board.attach_mouse(
        Mouse(
            mouse_board_pos,
            mouse_tile,
            pygame.mouse.get_pressed()
        )
    )

    mouse = board.get_mouse()



    if mouse.get_left_click():
        if mouse.get_index() and not clicked:
            clicked = True
            takeable = []
            moveable = []
            for m in moves:
                for n in m:
                    if not n.is_canceled():
                        moveable.append(n)
            for t in takes:
                for n in t:
                    if not n.is_canceled():
                        takeable.append(n)
            moving = []
            taking = []
            for n in takeable:
                if n.pos == mouse_tile:
                    taking.append(n)
            for n in moveable:
                if n.pos == mouse_tile:
                    moving.append(n)
            if len(moving) > 0:
                # print(selected_pos)
                board.get_piece_at(*selected_pos).move(mouse_tile)
                moves = []
                takes = []
            elif len(taking) > 0:
                # print(selected_pos)
                board.get_piece_at(*selected_pos).take(mouse_tile)
                moves = []
                takes = []
            elif board.get_piece_at(*mouse_tile):
                # print(mouse.get_index())
                selected_piece = board.get_piece_at(*mouse_tile)
                if selected_piece is not None:
                    moves = board.get_piece_at(*mouse_tile).get_moves()
                    takes = board.get_piece_at(*mouse_tile).get_takes()
                else:
                    moves, takes = [], []
            selected_pos = mouse_tile
    elif mouse.get_right_click() and debugging:
        if mouse.get_index() and not clicked:
            clicked = True
            piece = board.get_piece_at(*mouse_tile)
            print(f"""
---------------------------------------------
---------------- PIECE DEBUG ----------------
---------------------------------------------
    Position    : {[*mouse_tile]}
    Name        : {piece.name}
    Piece ID    : {piece.piece_id}
    Colour      : {piece.colour}
    Moves Count : {piece.move_count}
---------------------------------------------
"""
            )
    else:
        clicked = False

    if mouse_tile:
        board_display[0].fill(Vector3(255, 0, 0), (flip_coordinate(mouse_tile) * tile_size, Vector2(tile_size * 0.2)))

    win.blit(*board_display)

    pygame.display.flip()

    # board.move(pos1, pos2)
