import pygame
import random
import datetime
from ant import *
from logic import *


vision = 1 #usa isso
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

ants = [Ant(grid) for i in range(200)]
dead_ants = [DeadAnt(dead_grid) for i in range(700)]


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
    
    random.seed(str(datetime.datetime.now()))
    iterations = 200_000
    done = False
    move(ants, dead_ants, grid, dead_grid, height, width, vision)
    show_grid()
    pygame.image.save(gridDisplay, "experimento_visao_{}_iteracoes_{}_inicial.png".format(vision, iterations))

    for c in range(0, iterations):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        if done == True:break
        move(ants, dead_ants, grid, dead_grid, height, width, vision)
        #show_grid()
    while len(ants) > 0 and done == False:
        moveEnd(ants,dead_ants,grid,dead_grid,height,width,vision)
        #show_grid()

    show_grid()
    # dead_ant_count = 0
    # size = len(dead_grid)
    # for i in range(0, size):
    #     for j in range(0, size):
    #         if dead_grid[i][j] == 2:
    #             dead_ant_count += 1
    # print(dead_ant_count)
    pygame.image.save(gridDisplay, "experimento_visao_{}_iteracoes_{}_final.png".format(vision, iterations))
    # while True:
    #chama funcao que faz as formigas vazias sumirem e as formigas carregadas rodarem ate dropar
    pygame.quit()
