import pygame
from PIL import Image
import random
from tiles import generate

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.openings = [False, False, False, False]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.render = Image.new('RGB', (self.width, self.height), (255, 255, 255, 0))

        self.clock = pygame.time.Clock()
        self.running = True

        self.res = 20
        self.cells = []
        self.path = []
        self.scene = "walk"

        self.tiles = generate()

        for i in range(self.height // self.res):
            self.cells.append([])
            for j in range(self.width // self.res):
                self.cells[i].append(Cell(j, i))
        self.current = self.cells[0][0]
    
    def get_surface(self, texture: Image):
        return pygame.image.fromstring(texture.tobytes(), texture.size, texture.mode)

    def regenerate(self):
        self.cells = []
        for i in range(self.height // self.res):
            self.cells.append([])
            for j in range(self.width // self.res):
                self.cells[i].append(Cell(j, i))
        self.current = self.cells[0][0]
        self.path = []

    def valid(self, x, y):
        if x >= 0 and x < (self.width // self.res)-1 and y >= 0 and y < (self.height // self.res)-1:
            return self.cells[y][x].openings == [False, False, False, False]
            # return True

    def get_neighbors(self, x, y):
        neighbours = []
        if self.valid(x, y - 1):
            neighbours.append(self.cells[y - 1][x])
        if self.valid(x + 1, y):
            neighbours.append(self.cells[y][x + 1])
        if self.valid(x, y + 1):
            neighbours.append(self.cells[y + 1][x])
        if self.valid(x - 1, y):
            neighbours.append(self.cells[y][x - 1])
        
        return neighbours if len(neighbours) > 0 else None
    
    def walk(self):
        new = self.get_neighbors(self.current.x, self.current.y)
        if new:
            self.current = random.choice(new)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.regenerate()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.walk()

            self.render = Image.new('RGB', (self.width, self.height), (255, 255, 255, 0))
            self.screen.fill((255, 255, 255))

            self.cells[self.current.y][self.current.x].openings = [True, True, True, True]

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
                    else:
                        if openings!="a":
                            pygame.draw.circle(self.screen, (0, 0, 0, 10), (x * self.res + self.res // 2, y * self.res + self.res // 2), self.res // 3)
            pygame.draw.circle(self.screen, (255, 0, 0), ((self.current.x * self.res) + self.res // 2, (self.current.y * self.res) + self.res // 2), self.res // 3)
            n = self.get_neighbors(self.current.x, self.current.y)
            if n:
                for cell in n:
                    pygame.draw.circle(self.screen, (0, 255, 0), (cell.x * self.res + self.res // 2, cell.y * self.res + self.res // 2), self.res // 3)
            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()