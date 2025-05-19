import pygame
import json
from classes import AttributeDict, Board, GeneratedPiece


def load_json(file_path) -> dict:
    with open(file_path) as file:
        data: dict = json.load(file)
    return data


def save_data(file_path, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


config = AttributeDict(load_json("config.json"))

for piece_config_key in config.pieces:
    piece_config_key: str
    piece_config: AttributeDict = config.pieces[piece_config_key]
    print(GeneratedPiece(piece_config, piece_config_key))
