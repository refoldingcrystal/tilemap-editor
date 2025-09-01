import json
import os
import re
import pygame


def pos2str(pos):
    return str(pos[0]) + ';' + str(pos[1])

def str2pos(pos):
    pos = pos.split(';')
    return (int(pos[0]), int(pos[1]))


class Tilemap:
    def __init__(self, surf):
        self.draw_grid = True
        self.surf = surf
        self.tilemap = {}
        self.tile_size = 50
        self.tile_type = 1
        self.colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (0, 255, 255),
            (255, 0, 255),
            (255, 255, 0)
        ]

    def change_zoom(self, movement):
        self.tile_size = max(10, min(200, self.tile_size + movement * 5))

    def load(self, filename):
        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as f:
                    self.tilemap = json.load(f)
            except Exception:
                return False
            for tile_pos in self.tilemap.copy():
                if re.fullmatch(r"^[+-]?\d+;[+-]?\d+$", tile_pos) is None:
                    del self.tilemap[tile_pos]
                elif not isinstance(self.tilemap[tile_pos], int):
                    del self.tilemap[tile_pos]
                elif self.tilemap[tile_pos] not in range(1, len(self.colors) + 1):
                    del self.tilemap[tile_pos]

        return True

    def clear(self):
        self.tilemap = {}

    def change_tile_type(self, movement):
        self.tile_type = (self.tile_type + movement - 1) % len(self.colors) + 1
    
    def mouse2pos(self, m_pos, offset=[0,0]):
        return ((m_pos[0] + offset[0]) // self.tile_size, (m_pos[1] + offset[1]) // self.tile_size)

    def add(self, m_pos, offset):
        self.tilemap[pos2str(self.mouse2pos(m_pos, offset))] = self.tile_type

    def remove(self, m_pos, offset):
        pos = pos2str(self.mouse2pos(m_pos, offset))
        if pos in self.tilemap:
            del self.tilemap[pos]

    def render(self, m_pos, offset):
        for tile_pos in self.tilemap:
            pos = str2pos(tile_pos)
            rect = (pos[0] * self.tile_size - offset[0], pos[1] * self.tile_size - offset[1],
                    self.tile_size, self.tile_size)
            color = self.colors[self.tilemap[tile_pos] - 1]
            pygame.draw.rect(self.surf, color, rect)

        if self.draw_grid:
            for x in range(self.surf.get_width() // self.tile_size + 2):
                pygame.draw.line(self.surf, (200, 200, 200),
                                (x * self.tile_size - offset[0] % self.tile_size, 0),
                                (x * self.tile_size - offset[0] % self.tile_size, self.surf.get_height()))
            for y in range(self.surf.get_height() // self.tile_size + 2):
                pygame.draw.line(self.surf, (200, 200, 200),
                                (0, y * self.tile_size - offset[1] % self.tile_size),
                                (self.surf.get_width(), y * self.tile_size - offset[1] % self.tile_size))
            # does not work
            pygame.draw.line(self.surf, (200, 200, 200), (-offset[0], 0),
                             (-offset[0], self.surf.get_height()), width=3)
            pygame.draw.line(self.surf, (200, 200, 200), (0, -offset[1]),
                             (self.surf.get_width(), -offset[1]), width=3)
            
            pygame.draw.circle(self.surf, (200, 200, 200), (-offset[0], -offset[1]), radius=5)
        
        pos = self.mouse2pos(m_pos, offset)
        rect = (pos[0] * self.tile_size - offset[0], pos[1] * self.tile_size - offset[1],
                self.tile_size, self.tile_size)
        color = self.colors[self.tile_type - 1]
        pygame.draw.rect(self.surf, color, rect, width=5)

    def export(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.tilemap, file)
        print(f"Exported to '{filename}'")