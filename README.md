# Tilemap editor

Simple tool to create tilemaps

## Keybinds

`c` - clear canvas

`g` - toggle grid

`e` - export (defaults to `map.json`)

`lmb` - draw

`rmb` - erase

`mmb` - move around

`scroll` - change tile type

## Output format

map is exported as json

each non-blank tile is represented by its position and tile type

```json
"x;y": "type"
```

example smiley face

```json
{"1;0": 1, "1;1": 1, "3;0": 1, "3;1": 1, "0;3": 1, "1;4": 1, "2;4": 1, "3;4": 1, "4;3": 1}
```

## Usage

run with python

`python3 main.py`

alternatively provide name for exporting

`python3 main.py map.json`
