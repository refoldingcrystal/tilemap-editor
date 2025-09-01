import pygame


class Colors:
    def __init__(self, surf):
        self.surf = surf
        self.tile_type = 1
        self.colors = [
            (255, 0, 77),
            (0, 228, 54),
            (41, 173, 255),
            (255, 119, 168),
            (255, 236, 39)
        ]
        self.rects = []
        for i in range(len(self.colors)):
            self.rects.append(pygame.Rect(5, i * 60 + 5, 50, 50))

    def color(self, tile_type=None):
        if tile_type == None:
            return self.colors[self.tile_type - 1]
        return self.colors[tile_type - 1]
    
    def change_tile_type(self, tile_type):
        if 0 < tile_type <= len(self.colors):
            self.tile_type = tile_type

    def render(self, m_pos, pressed, draw):
        rect = pygame.Rect(0, 0, 60, self.surf.get_height())
        pygame.draw.rect(self.surf, (30, 30, 30), rect)
        for i, rect in enumerate(self.rects):
            pygame.draw.rect(self.surf, self.colors[i], rect, border_radius=10)
        if draw:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(m_pos):
                    pygame.draw.rect(self.surf, (30, 30, 30), rect, border_radius=10, width=2)
                    if pressed:
                        self.tile_type = i + 1
        pygame.draw.rect(self.surf, (30, 30, 30), self.rects[self.tile_type - 1], border_radius=10, width=5)
        

        