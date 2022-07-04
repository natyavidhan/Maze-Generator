import pygame
from PIL import Image
import random
from tiles import generate

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
        self.screen = pygame.display.set_mode((600, 400))
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.render = Image.new('RGB', (self.width, self.height), (255, 255, 255, 0))

        self.clock = pygame.time.Clock()
        self.running = True

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

    def valid(self, x, y):
        if x >= 0 and x <= (self.width // self.res)-1 and y >= 0 and y <= (self.height // self.res)-1:
            return not self.cells[y][x].tried

    def get_neighbors(self, x, y):
        neighbours = []
        s = self.cells[y][x]
        if self.valid(x, y - 1) and not s.openings[2]:
            neighbours.append(self.cells[y - 1][x])
        if self.valid(x + 1, y) and not s.openings[3]:
            neighbours.append(self.cells[y][x + 1])
        if self.valid(x, y + 1) and not s.openings[0]:
            neighbours.append(self.cells[y + 1][x])
        if self.valid(x - 1, y) and not s.openings[1]:
            neighbours.append(self.cells[y][x - 1])
        
        return neighbours if len(neighbours) > 0 else None

    def open_way(self, old, new):
        x = new.x - old.x
        y = new.y - old.y
        if x == 1:
            old.openings[3] = True
            new.openings[1] = True
        elif x == -1:
            old.openings[1] = True
            new.openings[3] = True
        elif y == 1:
            old.openings[0] = True
            new.openings[2] = True
        elif y == -1:
            old.openings[2] = True
            new.openings[0] = True
    
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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.regenerate()


            self.render = Image.new('RGB', (self.width, self.height), (255, 255, 255, 0))
            self.screen.fill((255, 255, 255))

            if len(self.path) < (self.width // self.res) * (self.height // self.res):
                if self.scene == "walk":
                    self.walk()

            for y, row in enumerate(self.cells):
                for x, cell in enumerate(row):
                    openings = ""
                    openings += "u" if cell.openings[0] else ""
                    openings += "r" if cell.openings[1] else ""
                    openings += "d" if cell.openings[2] else ""
                    openings += "l" if cell.openings[3] else ""
                    openings = "b" if openings == "urdl" else openings
                    openings = "a" if openings == "" else openings
                    if self.scene == "grid":
                        self.render.paste(self.tiles[openings], (x * self.res, y * self.res))
                        self.screen.blit(self.get_surface(self.render), (0, 0))

            for index, cell in enumerate(self.path):
                if index > 0:
                    pygame.draw.line(self.screen, (0, 0, 0), (self.path[index-1].x * self.res + self.res // 2, self.path[index-1].y * self.res + self.res // 2), (cell.x * self.res + self.res // 2, cell.y * self.res + self.res // 2), self.res // 4)
                pygame.draw.circle(self.screen, (0, 0, 0), (cell.x * self.res + self.res // 2, cell.y * self.res + self.res // 2), self.res // 8)

            pygame.draw.circle(self.screen, (0, 0, 0), ((self.current.x * self.res) + self.res // 2, (self.current.y * self.res) + self.res // 2), self.res // 3)

            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()