# Python Chess
This project contains my 3rd attempt at making chess with python, the other 2 probably wont be put on github

## Files
### The following lines describe what each file does
* main.py - This file is the main logic for the game, as well as the main loop, and managing inputs
* defaults.py - This file is the default functions for each event
* classes.py - All the classes for the project, like pieces, the board, and events
* config.json - The config for the pieces, this is used to make a scafold of the basic peace movement, the board setup, and most likely debuging logging
* Config Format.json - This is a schema for the config.json format, I'm not the best at schemas, so it's not perfect, but ok

## Files to be added
* Assets/* - this will contain all the images, and will load all the images in this directory into a dictionary that contains all the images, in the format of Assets["directory"]["directory or filename"]...
* functions.py - This will contain all the functions for the events, which will be added to a dictinary, most likely called "EventHandlers", and the key, (provided in the config) will be used to choose the function

## Events
* :P i'll do this later