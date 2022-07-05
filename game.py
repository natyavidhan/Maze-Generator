import pygame
from PIL import Image
import random
from tiles import generate
import time
from tkinter import filedialog

pygame.init()
pygame.font.init()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.openings = [False, False, False, False]
        self.tried = False

    def reset(self):
        self.openings = [False, False, False, False]
        self.tried = False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Maze Generator")
        self.height = self.screen.get_height()-100
        self.width = self.screen.get_width()
        self.render = pygame.Surface((self.width, self.height))
        self.ui = pygame.Surface((600, 100))

        self.clock = pygame.time.Clock()
        self.running = True
        self.start_time = time.time()
        self.end_time = None
        self.total_steps = 0
        self.exported = [False, False]

        self.res = 100
        self.cells = [[Cell(x, y) for x in range(self.width // self.res)] for y in range(self.height // self.res)]
        self.scene = "walk"

        self.tiles = generate()

        self.current = self.cells[0][0]
        self.current.tried = True
        self.path = [self.current]
    
    def get_surface(self, texture: Image):
        return pygame.image.fromstring(texture.tobytes(), texture.size, texture.mode)

    def regenerate(self):
        self.cells = [[Cell(x, y) for x in range(self.width // self.res)] for y in range(self.height // self.res)]
        self.current = self.cells[0][0]
        self.path = [self.current]
        self.current.tried = True
        self.scene = "walk"
        self.start_time = time.time()
        self.end_time = None
        self.total_steps = 0
        self.exported = [False, False]

    def valid(self, x, y):
        if x >= 0 and x <= (self.width // self.res)-1 and y >= 0 and y <= (self.height // self.res)-1:
            return not self.cells[y][x].tried

    def get_neighbors(self, x, y):
        neighbours = []
        s = self.cells[y][x]
        if self.valid(x, y - 1) and not s.openings[0]:
            neighbours.append(self.cells[y - 1][x])
        if self.valid(x + 1, y) and not s.openings[1]:
            neighbours.append(self.cells[y][x + 1])
        if self.valid(x, y + 1) and not s.openings[2]:
            neighbours.append(self.cells[y + 1][x])
        if self.valid(x - 1, y) and not s.openings[3]:
            neighbours.append(self.cells[y][x - 1])
        
        return neighbours if len(neighbours) > 0 else None

    def change(self, old, new, a, b):
        old.openings[a] = True
        new.openings[b] = True

    def open_way(self, old, new):
        x = new.x - old.x
        y = new.y - old.y
        if x == 1:
            self.change(old, new, 1, 3)
        elif x == -1:
            self.change(old, new, 3, 1)
        elif y == 1:
            self.change(old, new, 2, 0)
        elif y == -1:
            self.change(old, new, 0, 2)

    def uniform(self):
        old_path = self.path
        self.path = []
        for cell in old_path:
            cell.reset()
            self.path.append(cell)

        old = old_path[0]
        for i in range(1, len(old_path)):
            new = old_path[i]
            self.open_way(old, new)
            old = new
            self.path.append(new)
            

    
    def walk(self):
        new = self.get_neighbors(self.current.x, self.current.y)
        if new:
            old = self.current
            self.current = random.choice(new)
            self.open_way(old, self.current)
            self.path.append(self.current)
            self.current.tried = True
        elif len(self.path) > 1:
            stuck = self.path.pop()
            stuck.reset()
            self.current = self.path[-1]
        self.total_steps += 1
    
    def export(self):
        folder = filedialog.askdirectory()
        if folder:
            raw_img = pygame.image.tostring(self.render, "RGB")
            img = Image.frombytes("RGB", (self.width, self.height), raw_img)
            img.save(folder + "/" + str(time.time()) + ".png")

    def render_ui(self):
        self.ui.fill((255, 255, 255))
        pygame.draw.rect(self.ui, (0, 0, 0), (0, 0, 600, 100), 5)
        font = pygame.font.SysFont('Consolas', 20)
        total_time = self.end_time if self.end_time else time.time() 
        total_time -= self.start_time

        self.ui.blit(font.render(f'Length of Path: {len(self.path)}', True, (0, 0, 0)), (10, 10))
        self.ui.blit(font.render(f'Current Process: {self.scene}', True, (0, 0, 0)), (10, 35))
        self.ui.blit(font.render(f'Time Spent: {round(total_time, 2)}', True, (0, 0, 0)), (10, 60))
        self.ui.blit(font.render(f'Total Steps: {self.total_steps}', True, (0, 0, 0)), (275, 10))

        self.screen.blit(self.ui, (0, 400))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.regenerate()


            self.render.fill((255, 255, 255))
            self.screen.fill((255, 255, 255))

            if len(self.path) < (self.width // self.res) * (self.height // self.res):
                if self.scene == "walk":
                    self.walk()
            else:
                if self.end_time is None:
                    self.end_time = time.time()
                    self.uniform()
                    self.scene = "grid"

            if self.scene == "grid":
                for cell in self.path:
                    ox, oy = cell.x * self.res, cell.y * self.res
                    pygame.draw.rect(self.render, (0, 0, 0), (ox, oy, self.res, self.res), 5)
                    if cell.openings[0]:
                        pygame.draw.line(self.render, (255, 255, 255), (ox+5, oy+2.5), (ox+(self.res-6), oy+2.5), 5)
                    if cell.openings[1]:
                        pygame.draw.line(self.render, (255, 255, 255), ((ox+self.res)-2.5, oy+5), ((ox+self.res)-2.5, oy+(self.res-6)), 5)
                    if cell.openings[2]:
                        pygame.draw.line(self.render, (255, 255, 255), (ox+5, (oy+self.res)-2.5), (ox+(self.res-6), (oy+self.res)-2.5), 5)
                    if cell.openings[3]:
                        pygame.draw.line(self.render, (255, 255, 255), (ox+2.5, oy+5), (ox+2.5, oy+(self.res-6)), 5)
                font = pygame.font.SysFont('Consolas', 20)
                #start point
                pygame.draw.rect(self.render, (0, 255, 0), ((self.path[0].x * self.res)+5, (self.path[0].y * self.res)+5, self.res-10, self.res-10))
                text = font.render(f'Start', True, (0, 0, 0))
                r = text.get_rect()
                r.center = (self.path[0].x * self.res + self.res/2, self.path[0].y * self.res + self.res/2)
                self.render.blit(text, r)

                #end point
                pygame.draw.rect(self.render, (255, 0, 0), ((self.path[-1].x * self.res)+5, (self.path[-1].y * self.res)+5, self.res-10, self.res-10))
                text = font.render(f'End', True, (0, 0, 0))
                r = text.get_rect()
                r.center = (self.path[-1].x * self.res + self.res/2, self.path[-1].y * self.res + self.res/2)
                self.render.blit(text, r)
                self.screen.blit(self.render, (0, 0))
                if not self.exported[0]:
                    self.exported[0] = True
                elif not self.exported[1]:
                    self.exported[1] = True
                    self.export()


            elif self.scene == "walk":
                for index, cell in enumerate(self.path):
                    if index > 0:
                        pygame.draw.line(self.screen, (0, 0, 0), (self.path[index-1].x * self.res + self.res // 2, self.path[index-1].y * self.res + self.res // 2), (cell.x * self.res + self.res // 2, cell.y * self.res + self.res // 2), self.res // 4)
                        r = pygame.Rect(cell.x * self.res, cell.y * self.res, self.res//4, self.res//4)
                        r.center = ((cell.x * self.res + self.res // 2), (cell.y * self.res + self.res // 2))
                        pygame.draw.rect(self.screen, (0, 0, 0), r)

                pygame.draw.circle(self.screen, (0, 0, 0), ((self.current.x * self.res) + self.res // 2, (self.current.y * self.res) + self.res // 2), self.res // 4)

            self.render_ui()

            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()