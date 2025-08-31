import json
import os
import sys
import pygame


def close():
    pygame.quit()
    sys.exit()

def pos2str(pos):
    return str(pos[0]) + ';' + str(pos[1])

def str2pos(pos):
    pos = pos.split(';')
    return (int(pos[0]), int(pos[1]))


class Tilemap:
    def __init__(self, surf):
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

    def clear(self):
        self.tilemap = {}

    def change_tile_type(self, movement):
        self.tile_type = (self.tile_type + movement - 1) % len(self.colors) + 1
    
    def mouse2pos(self, m_pos):
        return (m_pos[0] // self.tile_size, m_pos[1] // self.tile_size)

    def add(self, m_pos):
        self.tilemap[pos2str(self.mouse2pos(m_pos))] = self.tile_type

    def remove(self, m_pos):
        pos = pos2str(self.mouse2pos(m_pos))
        if pos in self.tilemap:
            del self.tilemap[pos2str(self.mouse2pos(m_pos))]

    def render(self, m_pos):
        for tile_pos in self.tilemap:
            pos = str2pos(tile_pos)
            rect = (pos[0] * self.tile_size, pos[1] * self.tile_size,
                    self.tile_size, self.tile_size)
            color = self.colors[self.tilemap[tile_pos] - 1]
            pygame.draw.rect(self.surf, color, rect)
        
        pos = self.mouse2pos(m_pos)
        rect = (pos[0] * self.tile_size, pos[1] * self.tile_size,
                self.tile_size, self.tile_size)
        color = self.colors[self.tile_type - 1]
        pygame.draw.rect(self.surf, color, rect, width=5)

    def export(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.tilemap, file)
        

class Window:
    def __init__(self, filename='map.json'):
        self.filename = filename

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

        self.tilemap = Tilemap(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.tilemap.export(self.filename)
                    if event.key == pygame.K_c:
                        self.tilemap.clear()
                if event.type == pygame.MOUSEWHEEL:
                    self.tilemap.change_tile_type(event.y)

            pressed = pygame.mouse.get_pressed()
            m_pos = pygame.mouse.get_pos()
            if pressed[0]:
                self.tilemap.add(m_pos)
            elif pressed[2]:
                self.tilemap.remove(m_pos)
            
            self.screen.fill((20, 20, 20))
            self.tilemap.render(m_pos)
            pygame.display.update()

if len(sys.argv) < 2:
    print("Using 'map.json' as output file")
    filename = 'map.json'
# else:
#     filename = sys.argv[1]
# if os.path.isdir(filename):
#     print(f"'{filename} is a directory")
#     sys.exit()
# if os.path.isfile(filename):
#     print(f"'{filename}' is a file, continue anyway? [Y/n]")
#     if input() not in ['', 'y', 'Y']:
#         sys.exit()

Window(filename).run()

