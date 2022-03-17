import random
import os
import pygame
from tiles import generate
scale = 16
WIDTH, HEIGHT = 1200//scale, 600//scale

pygame.init()
namedTiles = {}
names = [
    'ud', 'rl', 'rd', 'ur', 'dl', 'ul', 
    'b', 'a', 
    'urd', 'udl', 'url', 'rdl',
    'r', 'l', 'd', 'u',
]
    
mep = []
def valid(x, y):
    return x >= 0 and x < WIDTH-1 and y >= 0 and y < HEIGHT-1

class Block:
    def __init__(self, x, y, openings = [False, False, False, False]):
        self.x = x
        self.y = y
        self.openings = openings
        
    def show(self):
        if self.openings[0]:
            if self.openings[1]:
                if self.openings[2]:
                    if self.openings[3]:
                        return 'a'
                    else:
                        return 'urd'
                elif self.openings[3]:
                    return 'url'
                else:
                    return 'ur'
            elif self.openings[2]:
                if self.openings[3]:
                    return 'udl'
                else:
                    return 'ud'
            elif self.openings[3]:
                return 'rd'
            else:
                return 'u'
        elif self.openings[1]:
            if self.openings[2]:
                if self.openings[3]:
                    return 'rdl'
                else:
                    return 'ul'
            elif self.openings[3]:
                return 'rl'
            else:
                return 'r'
        elif self.openings[2]:
            if self.openings[3]:
                return 'dl'
            else:
                return 'd'
        elif self.openings[3]:
            return 'l'
        else:
            return 'b'

    def getNeighbours(self):
        neighbours = []
        empty = [False, False, False, False]
        
        up     = mep[self.y - 1][self.x]
        right  = mep[self.y][self.x + 1]
        bottom = mep[self.y + 1][self.x]
        left   = mep[self.y][self.x - 1]
        
        if (up.openings == empty 
            and valid(self.x, self.y - 1)):
            neighbours.append(up)
        if (right.openings == empty 
            and valid(self.x + 1, self.y)):
            neighbours.append(right)
        if (bottom.openings == empty 
            and valid(self.x, self.y + 1)):
            neighbours.append(bottom)
        if (left.openings == empty 
            and valid(self.x - 1, self.y)):
            neighbours.append(left)
        
        return neighbours
            
    
def removeWalls(a, b):
    y = a.x - b.x
    x = a.y - b.y
    if x == 1:
        a.openings[3] = False
        b.openings[1] = False
    elif x == -1:
        a.openings[1] = False
        b.openings[3] = False
    elif y == 1:
        a.openings[0] = False
        b.openings[2] = False
    elif y == -1:
        a.openings[2] = False
        b.openings[0] = False

screen = pygame.display.set_mode((WIDTH*scale, HEIGHT*scale))
clock = pygame.time.Clock()
current = None
stack = []

def doThing():
    global current
    if current:
        n = current.getNeighbours()
        if len(n) != 0:
            last = current
            current = random.choice(n)
            stack.append(current)
            current.openings = [True, True, True, True]
            removeWalls(last, current)
        elif len(stack) != 0:
            current = stack.pop()
            
    for i in mep:
        for j in i:
            screen.blit(namedTiles[j.show()], (j.x*(scale), j.y*(scale)))
            
def refresh():
    global mep, current
    mep = [[Block(i, j) for i in range(WIDTH)] for j in range(HEIGHT)]
    current = mep[0][0]

refresh()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            refresh()
        doThing()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    generate()
    for i in names:
        namedTiles[i] = pygame.image.load(f"assets/{i}.png")
        namedTiles[i] = pygame.transform.scale(namedTiles[i], (scale, scale))
    main()