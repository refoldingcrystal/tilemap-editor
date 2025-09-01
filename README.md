# Tilemap editor

Simple tool to create tilemaps

Currently does not support textures

## Keybinds

`c` - clear canvas

`g` - toggle grid

`e` - export (defaults to `map.json`)

`keys 1 - 6` - change color

`left mouse button` - draw

`right mouse button` - erase

`middle mouse button` - move around

`scroll` - zoom in/out

## Output format

Map is exported as json

Each non-blank tile is represented by its position and tile type

```json
"x;y": "type"
```

Example smiley face

```json
{"1;0": 1, "1;1": 1, "3;0": 1, "3;1": 1, "0;3": 1, "1;4": 1, "2;4": 1, "3;4": 1, "4;3": 1}
```

## Usage

Run with python, map will be exported to `map.json`

`python3 main.py`

Alternatively provide name for exporting

`python3 main.py map.json`
