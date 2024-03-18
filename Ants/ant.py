import random


class Ant:
    def __init__(self, coords, matrix = list(list)):
        
        self.carrying = False
        self.dead_ants =  0 #quantidade de formigas mortas ao redor de uma dada formiga
        self.exists = False

        while not self.exists:
            self.x = random.randint(0, len(matrix) - 1)
            self.y = random.randint(0, len(matrix[0]) - 1)

            if(matrix)