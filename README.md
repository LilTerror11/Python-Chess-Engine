# Python Chess
This project contains my 3rd attempt at making chess with python, the other 2 probably wont be put on github

## Files
### The following lines describe what each file does
* `main.py` - This file is the main logic for the game, as well as the main loop, and managing inputs
* `defaults.py` - This file is the default functions for each event
* `classes.py` - All the classes for the project, like pieces, the board, and events
* `config.json` - The config for the pieces, this is used to make a scafold of the basic peace movement, the board setup, and most likely debuging logging
* `Config Format.json` - This is a schema for the config.json format, I'm not the best at schemas, so it's not perfect, but ok

### This file has been added
* `functions.py` - This will contain all the functions for the events, which will be added to a dictinary, most likely called "EventHandlers", and the key, (provided in the config) will be used to choose the function


## Files to be added
* `Assets/*` - this will contain all the images, and will load all the images in this directory into a dictionary that contains all the images, in the format of `Assets["directory"]["directory or filename"]...`
    #### This has been changed to `Assets["relative path"]`
___
## Events
#### There are 10 different events, 4 of these are in 'move \ take' pairs
A 'Child' event is a event that is fed into the 'Parent' event
### Paired Events
- #### `move` / `take`
   - This event is called whenever a piece is selected, this event manages all the squares that can be taken / moved to
  - #### These are child events of `select` and `on_event`
  - #### These events are technically parent events of `tile_move` and `tile_take` respectively
- #### `tile_move` / `tile_take`
  - These events are called on move / take generation, for each tile in the move / take, this event is called to decide if the move / take should continue, this event
  - #### These events are technically child events for `move` and `take` respectively and child events of `on_event`
  :P i'll continue this later

___
### Lazy Event Listing :P

* `move` / `take`
* `tile_move` / `tile_take`
* `setup`
* `select`
* `on_move`, `on_attack`, `on_taken`
* `on_event`