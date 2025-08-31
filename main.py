import os
import sys
import pygame

from tilemap import Tilemap
        

class Window:
    def __init__(self, filename='map.json'):
        self.filename = filename

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

        self.tilemap = Tilemap(self.screen)
        if not self.tilemap.load(self.filename):
            print(f"Could not load '{filename}'")


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.tilemap.export(self.filename)
                    if event.key == pygame.K_c:
                        self.tilemap.clear()
                    if event.key == pygame.K_g:
                        self.tilemap.draw_grid ^= True
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
else:
    filename = sys.argv[1]
if os.path.isdir(filename):
    print(f"'{filename} is a directory")
    sys.exit()

Window(filename).run()

