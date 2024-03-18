import random


class Ant:
    def __init__(self , grid = list[list[int]]):
        
        self.x = -1
        self.y = -1
        self.is_carrying = False
        self.dead_ants_around =  0 #quantidade de formigas mortas ao redor de uma dada formiga
        self.exists = False


        #enquanto não achar uma célula válida, continua tentando
        while self.exists == False:
            self.x = random.randint(0, len(grid) - 1)
            self.y = random.randint(0, len(grid[0]) - 1)

            if grid[self.x] [self.y] == 0:
                grid[self.x] [self.y] = 1
                self.exists = True

class DeadAnt:
    def __init__(self, grid = list[list[int]]):
        
        self.x = -1
        self.y = -1
        self.carried = False
        self.carrier = None
        self.exists = False
        
        #enquanto não achar uma célula válida, continua tentando
        while self.exists == False:
            self.x = random.randint(0, len(grid) - 1)
            self.y = random.randint(0, len(grid[0]) - 1)

            if grid[self.x] [self.y] == 0:
                grid[self.x] [self.y] = 2
                self.exists = True
