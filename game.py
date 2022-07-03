import pygame
from PIL import Image
import random
from tiles import generate

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.openings = [random.choice([True, False]) for i in range(4)]

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

        self.tiles = generate()

        for i in range(self.height // self.res):
            self.cells.append([])
            for j in range(self.width // self.res):
                self.cells[i].append(Cell(i, j))
    
    def get_surface(self, texture: Image):
        return pygame.image.fromstring(texture.tobytes(), texture.size, texture.mode)

    def regenerate(self):
        self.cells = []
        for i in range(self.height // self.res):
            self.cells.append([])
            for j in range(self.width // self.res):
                self.cells[i].append(Cell(i, j))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.regenerate()

            self.render = Image.new('RGB', (self.width, self.height), (255, 255, 255, 0))
            
            for y, row in enumerate(self.cells):
                for x, cell in enumerate(row):
                    openings = ""
                    openings += "u" if cell.openings[0] else ""
                    openings += "r" if cell.openings[1] else ""
                    openings += "d" if cell.openings[2] else ""
                    openings += "l" if cell.openings[3] else ""
                    openings = "b" if openings == "urdl" else openings
                    openings = "a" if openings == "" else openings
                    self.render.paste(self.tiles[openings], (x * self.res, y * self.res))
            self.screen.blit(self.get_surface(self.render), (0, 0))

            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()