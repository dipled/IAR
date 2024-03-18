import pygame
import random
import datetime
from ant import *
from logic import *

color = (255, 0, 0)
gridDisplay = pygame.display.set_mode((700, 700))

height = 70
width = 70
grid = [[0 for i in range(width)] for i in range(height)]
dead_grid = [[0 for i in range(width)] for i in range(height)]

grid_cell_height = 10
grid_cell_width = 10

ant_height = 10
ant_width = 10

ants = [Ant(grid) for i in range(5)]
dead_ants = [DeadAnt(dead_grid) for i in range(500)]


def createSquare(x, y, color):
    pygame.draw.rect(gridDisplay, color, [
                     x, y, grid_cell_width, grid_cell_height])


def show_grid():
    y = 0


    for row in grid:
        x = 0  
        row_len = 0
        for item in row:
            
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            if item == 1:
                createSquare(x, y, (0, 0, 0))

            # for ever item/number in that row we move one "step" to the right
            x += grid_cell_width
            row_len += 1
       
        y += grid_cell_width   # for every new row we move one "step" downwards
    
    y = 0
    for line in dead_grid:
        x = 0
        for dead_ant in line:
              
            if dead_ant == 2:
                createSquare(x, y, (255, 172, 28))
            x += grid_cell_width

        y += grid_cell_width
    pygame.display.update()

if __name__ == '__main__':
    
    done = False
    contf = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        random.seed(str(datetime.datetime.now()))
        move(ants, dead_ants, grid, dead_grid, height, width)
    # while True:
        show_grid()
    pygame.quit()
