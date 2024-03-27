import pygame
import random
import datetime
import math


grid_display = pygame.display.set_mode((600, 600))
color = (255, 0, 0)
grid_display.fill(color)
height = 60
vision = 1
width = 60
α = 30
k1 = 0.35
k2 = 0.65
grid = [[0 for _ in range(width)] for _ in range(height)]
data_grid = [[0 for _ in range(width)] for _ in range(height)]

grid_cell_height = 10
grid_cell_width = 10

ant_height = 10
ant_width = 10
num_ants = 25

class Ant:
    def __init__(self, x, y, grid):
        self.exists = False
        self.is_carrying = False
        self.data_around = 0
        self.carrying = None
        while not self.exists:
            self.x = random.randint(0, height - 1)
            self.y = random.randint(0, width - 1)
            if grid[self.x][self.y] == 0:
                self.exists = True
                grid[self.x][self.y] = self


class Data:
    def __init__(self, grid,value_x,value_y,tag):
        self.carrier = None
        self.carried = False
        self.exists = False
        self.value_x = value_x
        self.value_y = value_y
        self.tag = tag
        while not self.exists:
            self.x = random.randint(0, height - 1)
            self.y = random.randint(0, width - 1)
            if grid[self.x][self.y] == 0:
                self.exists = True
                grid[self.x][self.y] = self


data_list = []
arc = open("data2.txt", "r")
for x in arc:
    data_txt = x.split("/")
    data1 = Data(data_grid, float(data_txt[0]), float(data_txt[1]), int(data_txt[2]))
    data_list.append(data1)

ants = [Ant(1, 2, grid) for _ in range(num_ants)]


def createSquare(x, y, color):
    pygame.draw.rect(grid_display, color, [
                     x, y, grid_cell_height, grid_cell_width])


def get_element(grid, line, row):
    return grid[line % height][row % width]


def data_similarity(grid, ant: Ant):
    elements = get_elements_around(ant, data_grid)
    # print(ant.data_around)
    carried_data = ant.carrying
    local_data = data_grid[ant.x][ant.y]
    sum_distance = 0
    for element in elements:

        sum_element = 0

        if carried_data:
            sum_element = (1 - (math.sqrt((carried_data.value_x - element.value_x) ** 2 + (carried_data.value_y - element.value_y) ** 2)) / α)

        elif local_data != 0:
            sum_element = (1 - (math.sqrt((local_data.value_x - element.value_x) ** 2 + (local_data.value_y - element.value_y) ** 2)) / α)

        sum_distance += sum_element

    similarity = sum_distance
    # print(ant.data_around)
    if similarity > 0:
        # print(ant.data_around)
        return similarity/(3 ** 2)
        # return similarity/(ant.data_around ** 2)
    else:
        return 0

def pick(ant: Ant, grid):
    if not ant.is_carrying and (data_grid[ant.x][ant.y]) != 0:
        fx = data_similarity(grid, ant)
        odds = (k1/(k1+fx)) ** 2
        if random.uniform(0, 1) <= odds:
            ant.is_carrying = True
            data_grid[ant.x][ant.y] = 0
            for data in data_list:
                if data.x == ant.x and data.y == ant.y:
                    data.carrier = ant
                    data.carried = True
                    ant.carrying = data
        

def drop(ant: Ant, grid):
    # odds = ant.data_around / 7.7
    if ant.is_carrying and (data_grid[ant.x][ant.y]) == 0:
        fx = data_similarity(grid, ant)
        odds = (fx/(k2+fx)) ** 2

        if random.uniform(0, 1) <= odds:
            ant.is_carrying = False
            data_grid[ant.x][ant.y] = ant.carrying

            for data in data_list:
                if data.carrier == ant:
                    data.carried = False
                    data.carrier = None
                    ant.carrying = None
                    data.x = ant.x
                    data.y = ant.y


def get_elements_around(ant: Ant, grid):
    ant.data_around = 0
    next_list = []
    for i in range(1,vision + 1):
        next = get_element(grid, ant.x - i, ant.y)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x + i, ant.y)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x, ant.y - i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x, ant.y + i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x + i, ant.y + i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x - i, ant.y - i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x - i, ant.y + i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
        next = get_element(grid, ant.x + i, ant.y - i)
        if next != 0:
            next_list.append(next)
            ant.data_around = ant.data_around + 1
    # print(ant.data_around)
    return next_list

def update_data(data_list, grid):
    for data in data_list:
        if grid[data.x][data.y] == 0 and not data.carried:
            grid[data.x][data.y] = data


def move_border(ant: Ant, grid, direction):
    if ant.x == 0 and direction == 1:
        if grid[height - 1][ant.y] == 0:
            grid[ant.x][ant.y] = 0
            ant.x = height - 1
            grid[ant.x][ant.y] = 1

    if ant.x == height - 1 and direction == 2:
        if grid[0][ant.y] == 0:
            grid[ant.x][ant.y] = 0
            ant.x = 0
            grid[ant.x][ant.y] = 1
    if ant.y == 0 and direction == 3:


        if grid[ant.x][width - 1] == 0:
            grid[ant.x][ant.y] = 0
            ant.y = width - 1
            grid[ant.x][ant.y] = 1

    if ant.y == width - 1 and direction == 4:

        if get_element(grid, ant.x, 0) == 0:
            grid[ant.x][ant.y] = 0
            ant.y = 0
            grid[ant.x][ant.y] = 1


def move(ants: list[Ant], grid, end_of_program = False):
    cont = 0
    for ant in ants:
        direction = random.randint(1, 4)
        if direction == 1:
            if ant.x == 0:

                move_border(ant, grid, direction)
                # get_elements_around(ant, data_grid)
                pick(ant, grid)
                drop(ant, grid)

            else:
                if grid[ant.x - 1][ant.y] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.x = ant.x - 1
                    grid[ant.x][ant.y] = 1
                    # get_elements_around(ant, data_grid)
                    pick(ant, grid)
                    drop(ant, grid)

        if direction == 2:
            if ant.x == height - 1:

                move_border(ant, grid, direction)

                pick(ant, grid)
                drop(ant, grid)

            else:
                if grid[ant.x + 1][ant.y] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.x = ant.x + 1
                    grid[ant.x][ant.y] = 1
                    # get_elements_around(ant, data_grid)
                    pick(ant, grid)
                    drop(ant, grid)

        if direction == 3:
            if ant.y == 0:

                move_border(ant, grid, direction)
                # get_elements_around(ant, data_grid)
                pick(ant, grid)
                drop(ant, grid)

            else:
                if grid[ant.x][ant.y - 1] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.y = ant.y - 1
                    grid[ant.x][ant.y] = 1
                    # get_elements_around(ant, data_grid)
                    pick(ant, grid)
                    drop(ant, grid)

        if direction == 4:
            if ant.y == width - 1:
                move_border(ant, grid, direction)
                # get_elements_around(ant, data_grid)
                pick(ant, grid)
                drop(ant, grid)

            else:
                if grid[ant.x][ant.y + 1] != 1:
                    grid[ant.x][ant.y] = 0
                    ant.y = ant.y + 1
                    grid[ant.x][ant.y] = 1
                    # get_elements_around(ant, data_grid)
                    pick(ant, grid)
                    drop(ant, grid)
        if ant.carrying == None and end_of_program == True:
            ants.remove(ant)
            grid[ant.x][ant.y] = 0
        # cont = cont + 1



def show_grid():
    y = 0

    colum_len = 0
    for row in grid:
        x = 0  
        row_len = 0
        for item in row:
            
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            if item == 1:
                createSquare(x, y, (0, 0, 0))
            x += grid_cell_height
            row_len = row_len + 1
      
        y += grid_cell_height  
    
    y = 0
    for line in data_grid:
        x = 0
        for data in line:
              
            if type(data) == Data:
                if data.tag == 1:
                    createSquare(x, y, (0, 255, 0))
                if data.tag == 2:
                    createSquare(x, y, (255, 255, 0))
                if data.tag == 3:
                    createSquare(x, y, (0, 255, 255))
                if data.tag == 4:
                    createSquare(x, y, (255, 0, 0))
                # if data.tag == 5:
                #     createSquare(x, y, (0, 0, 255))
                # if data.tag == 6:
                #     createSquare(x, y, (255, 0, 255))
                # if data.tag == 7:
                #     createSquare(x, y, (120, 120, 50))
                # if data.tag == 8:
                #     createSquare(x, y, (120, 0, 120))
                # if data.tag == 9:
                #     createSquare(x, y, (0, 120, 120))
                # if data.tag == 10:
                #     createSquare(x, y, (120, 50, 255))
                # if data.tag == 11:
                #     createSquare(x, y, (50, 120, 255))
                # if data.tag == 12:
                #     createSquare(x, y, (50, 255, 120))
                # if data.tag == 13:
                #     createSquare(x, y, (255, 120, 50))
                # if data.tag == 14:
                #     createSquare(x, y, (255, 50, 120))
                # if data.tag == 14:
                #     createSquare(x, y, (120, 50, 155))
            x += grid_cell_height

        y += grid_cell_height
    pygame.display.update()



if __name__ == '__main__':
    iterations = 2_000_000
    done = False
    contf = 0
    show_grid()
    pygame.image.save(grid_display, "experimento_visao_{}_iteracoes_{}_inicial.png".format(vision, iterations))
    random.seed(str(datetime.datetime.now()))
    for i in range(0, iterations):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        if done == True:break
        move(ants, grid)
        # show_grid()
        # if i % 1000 == 0:
        #     show_grid()


    while len(ants) > 0 and not done:
        pygame.event.get()
        move(ants, grid, True)
        show_grid()
    # show_grid()

    pygame.image.save(grid_display, "experimento_visao_{}_iteracoes_{}_final.png".format(vision, iterations))

    pygame.quit()
