import random
from ant import Ant, DeadAnt

def picks(ant: Ant, dead_grid: list[list[int]], dead_ants: list[DeadAnt]):
    odds = (1 - 1/50 * ant.dead_ants_around**2)
    if random.uniform(0, 1) <= odds and not ant.is_carrying and dead_grid[ant.x][ant.y] == 2:
        ant.is_carrying = True
        dead_grid[ant.x][ant.y] = 0
        for dead_ant in dead_ants:
            if dead_ant.x == ant.x and dead_ant.y == ant.y:
                dead_ant.carrier = ant
                dead_ant.carried = True

def drops(ant: Ant, dead_grid: list[list[int]], dead_ants: list[DeadAnt]):
    chance = 1/50 * ant.dead_ants_around**2
    if random.uniform(0, 1) <= chance and ant.is_carrying and dead_grid[ant.x][ant.y]!=2:
        ant.is_carrying = False
        dead_grid[ant.x][ant.y] = 2

        for dead_ant in dead_ants:
            if dead_ant.carrier == ant:
                dead_ant.carried = False
                dead_ant.carrier = None
                dead_ant.x = ant.x
                dead_ant.y = ant.y


def get_element(grid, x, y, height, width):
    return grid[x % height][y % width]


def get_vision(ant: Ant, grid: list[list[int]], height, width):
    ant.dead_ants_around = 0
    vision = 1

    next = get_element(grid, ant.x-vision, ant.y, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x+vision, ant.y, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x, ant.y-vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x, ant.y+vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x+vision, ant.y+vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x-vision, ant.y-vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x-vision, ant.y+vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1
    next = get_element(grid, ant.x+vision, ant.y-vision, height, width)
    if next == 2:
        ant.dead_ants_around = ant.dead_ants_around+1


def update_dead_ants(dead_ants: list[DeadAnt], grid = list[list[int]]):
    for dead_ant in dead_ants:
        if grid[dead_ant.x][dead_ant.y] == 0 and not dead_ant.carried:
            grid[dead_ant.x][dead_ant.y] = 2

def move_border(ant, grid, direction, height, width):
    if ant.x == 0 and direction == 1:
        if grid[height-1][ant.y] == 0:
            grid[ant.x][ant.y] = 0
            ant.x = height-1
            grid[ant.x][ant.y] = 1

    if ant.x == height-1 and direction == 2:
        if grid[0][ant.y] == 0:
            grid[ant.x][ant.y] = 0
            ant.x = 0
            grid[ant.x][ant.y] = 1
    if ant.y == 0 and direction == 3:


        if grid[ant.x][width-1] == 0:
            grid[ant.x][ant.y] = 0
            ant.y = width-1
            grid[ant.x][ant.y] = 1

    if ant.y == width-1 and direction == 4:

        if get_element(grid, ant.x, 0, height, width) == 0:
            grid[ant.x][ant.y] = 0
            ant.y = 0
            grid[ant.x][ant.y] = 1


def move(ants: list[Ant], dead_ants:list[DeadAnt], grid: list[list[int]], dead_grid: list[list[int]], height, width):
    cont = 0
    for ant in ants:
        direction = random.randint(1, 4)
        if direction == 1:
            if ant.x == 0:

                move_border(ant, grid, direction, height, width)
                get_vision(ant, dead_grid, height, width)
                picks(ant, dead_grid, dead_ants)
                drops(ant, dead_grid, dead_ants)

            else:
                if grid[ant.x-1][ant.y] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.x = ant.x - 1
                    grid[ant.x][ant.y] = 1
                    get_vision(ant, dead_grid, height, width)
                    picks(ant, dead_grid, dead_ants)
                    drops(ant, dead_grid, dead_ants)

        if direction == 2:
            if ant.x == width-1:

                move_border(ant, grid, direction, height, width)
                get_vision(ant, dead_grid, height, width)
                picks(ant, dead_grid, dead_ants)
                drops(ant, dead_grid, dead_ants)

            else:
                if grid[ant.x+1][ant.y] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.x = ant.x + 1
                    grid[ant.x][ant.y] = 1
                    get_vision(ant, dead_grid, height, width)
                    picks(ant, dead_grid, dead_ants)
                    drops(ant, dead_grid, dead_ants)

        if direction == 3:
            if ant.y == 0:

                move_border(ant, grid, direction, height, width)
                get_vision(ant, dead_grid, height, width)
                picks(ant, dead_grid, dead_ants)
                drops(ant, dead_grid, dead_ants)

            else:
                if grid[ant.x][ant.y-1] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.y = ant.y - 1
                    grid[ant.x][ant.y] = 1
                    get_vision(ant, dead_grid, height, width)
                    picks(ant, dead_grid, dead_ants)
                    drops(ant, dead_grid, dead_ants)

        if direction == 4:
            if ant.y == height-1:
                move_border(ant, grid, direction, height, width)
                get_vision(ant, dead_grid, height, width)
                picks(ant, dead_grid, dead_ants)
                drops(ant, dead_grid, dead_ants)

            else:
                if grid[ant.x][ant.y+1] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.y = ant.y + 1
                    grid[ant.x][ant.y] = 1
                    get_vision(ant, dead_grid, height, width)
                    picks(ant,dead_grid, dead_ants)
                    drops(ant, dead_grid, dead_ants)

        cont = cont+1

