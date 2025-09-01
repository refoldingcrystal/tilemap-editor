import os
import sys
import pygame

from colors import Colors
from tilemap import Tilemap
        

class Window:
    def __init__(self, filename='map.json'):
        self.filename = filename

        pygame.init()
        self.screen = pygame.display.set_mode((801, 601), pygame.RESIZABLE)
        pygame.display.set_caption("Tilemap editor")

        self.colors = Colors(self.screen)
        self.tilemap = Tilemap(self.screen, self.colors)
        if not self.tilemap.load(self.filename):
            print(f"Could not load '{filename}'")

        self.camera = [-self.screen.get_width() // 2, -self.screen.get_height() // 2]
        self.moving = False
        self.moving_start = None
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
                    match event.key:
                        case pygame.K_1:
                            self.colors.change_tile_type(1)
                        case pygame.K_2:
                            self.colors.change_tile_type(2)
                        case pygame.K_3:
                            self.colors.change_tile_type(3)
                        case pygame.K_4:
                            self.colors.change_tile_type(4)
                        case pygame.K_5:
                            self.colors.change_tile_type(5)
                        case pygame.K_6:
                            self.colors.change_tile_type(6)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False
                if event.type == pygame.MOUSEWHEEL:
                    self.tilemap.change_zoom(event.y)

            pressed = pygame.mouse.get_pressed()
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] > 60:
                if pressed[0]:
                    self.tilemap.add(m_pos, self.camera)
                if pressed[1]:
                    self.move_camera()
                elif pressed[2]:
                    self.tilemap.remove(m_pos, self.camera)
                
            if not pressed[1]:
                self.moving = False
            
            self.screen.fill((20, 20, 20))
            self.tilemap.render(m_pos, self.camera, canvas=(m_pos[0] > 60))
            self.colors.render(m_pos, pressed[0], canvas=(m_pos[0] > 60))
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

