import numpy as np
import pygame
from random import randint, randrange
from copy import deepcopy
from numba import njit

RES = WIDTH, HEIGHT = 1200, 675
TILE = 2
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = -1

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def set_glider_SE(current_state, x, y):
    pos = [(x, y), (x + 1, y + 1), (x - 1, y + 2), (x, y + 2), (x + 1, y + 2)]
    for i, j in pos:
        current_state[j][i] = 1
    return current_state


def set_glider_NW(current_state, x, y):
    pos = [(x, y), (x - 2, y - 1), (x - 2, y), (x - 2, y + 1), (x + 1, y - 1)]
    for i, j in pos:
        current_state[j][i] = 1
    return current_state


next_field = np.array([[0 for i in range(W)] for j in range(H)])

"""Arrange starting cell position HERE"""
# current_field = np.array([[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)])
current_field = np.array([[0 for i in range(W)] for j in range(H)])

for _ in range(500):
    i0, j0 = randrange(TILE, W // 2 + W // 4, TILE), randrange(TILE, H // 2)
    current_field = set_glider_SE(current_field, i0, j0)
    # i1, j1 = randrange(W // 2 - W // 4, W - TILE), randrange(H // 2, H - TILE)
    # current_field = set_glider_SE(current_field, i1, j1)


# current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)])


@njit(fastmath=True)
def check_cells(current_state, next_state):
    res = []

    for x in range(W):
        for y in range(H):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_state[j % H][i % W] == 1:
                        count += 1

            if current_state[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_state[y][x] = 1
                    res.append((x, y))
                else:
                    next_state[y][x] = 0
            else:
                if count == 3:
                    next_state[y][x] = 1
                    res.append((x, y))
                else:
                    next_state[y][x] = 0
    return next_state, res


while True:

    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    """Draw Grid"""
    # [pygame.draw.line(surface, pygame.Color('dimgray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    # [pygame.draw.line(surface, pygame.Color('dimgray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

    """draw life"""
    next_field, res = check_cells(current_field, next_field)
    [pygame.draw.rect(surface, pygame.Color('forestgreen'),
                      (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)

    print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)
