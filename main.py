import os
import sys
import pygame

from tilemap import Tilemap
        

class Window:
    def __init__(self, filename='map.json'):
        self.filename = filename

        pygame.init()
        self.screen = pygame.display.set_mode((801, 601), pygame.RESIZABLE)

        self.tilemap = Tilemap(self.screen)
        if not self.tilemap.load(self.filename):
            print(f"Could not load '{filename}'")

        self.camera = [-self.screen.get_width() // 2, -self.screen.get_height() // 2]
        self.moving = False
        self.moving_start = None
        self.ctrl = False
        self.fullscreen = False

    def move_camera(self):
        if not self.moving:
            self.moving = True
            self.moving_start = pygame.mouse.get_pos()
            self.camera_start = self.camera.copy()
        else:
            m_pos = pygame.mouse.get_pos()
            dx = self.moving_start[0] - m_pos[0]
            dy = self.moving_start[1] - m_pos[1]
            self.camera[0] = self.camera_start[0] + dx
            self.camera[1] = self.camera_start[1] + dy

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((801, 601), pygame.RESIZABLE)
                        else:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        self.fullscreen ^= True
                    if event.key == pygame.K_e:
                        self.tilemap.export(self.filename)
                    if event.key == pygame.K_c:
                        self.tilemap.clear()
                    if event.key == pygame.K_g:
                        self.tilemap.draw_grid ^= True
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False
                if event.type == pygame.MOUSEWHEEL:
                    if self.ctrl:
                        self.tilemap.change_zoom(event.y)
                    else:
                        self.tilemap.change_tile_type(event.y)

            pressed = pygame.mouse.get_pressed()
            m_pos = pygame.mouse.get_pos()
            if pressed[0]:
                self.tilemap.add(m_pos, self.camera)
            if pressed[1]:
                self.move_camera()
            elif pressed[2]:
                self.tilemap.remove(m_pos, self.camera)
                
            if not pressed[1]:
                self.moving = False
            
            self.screen.fill((20, 20, 20))
            self.tilemap.render(m_pos, self.camera)
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

