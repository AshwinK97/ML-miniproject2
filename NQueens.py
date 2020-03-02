# Mini Project 2
# Jasindan Rasalingam - 100584595
# Ashwin Kamalakannan - 100584423

class NQueens:
    def __init__(self):
        self.board = self.createBoard()
        self.solutions = []
        self.size = 8
        self.env = []
        self.goal = None
        self.goalIndex = -1

    def createBoard(self):
        board = [[0 for i in range(8)] for j in range(8)]
        return board

    def setBoard(self,board,gen):
        for i in range(self.size):
            board[gen[i]][i] = 1

    def genereteDNA(self):
        from random import shuffle
        DNA = list(range(self.size))
        shuffle(DNA)
        while DNA in self.env:
            shuffle(DNA)
        return DNA

    def initializeFirstGenereation(self):
        for i in range(100):
            self.env.append(self.genereteDNA())

    def fitness(self,gen):
        hits = 0
        board = self.createBoard()
        self.setBoard(board,gen)
        col = 0
        for dna in gen:
            try:
                for i in range(col-1,-1,-1):
                    if board[dna][i] == 1:
                        hits+=1
            except IndexError:
                print(gen)
                quit()
            for i,j in zip(range(dna-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            for i,j in zip(range(dna+1,self.size,1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            col+=1
        return hits

    def isGoalGen(self,gen):
        if self.fitness(gen) == 0:
            return True
        return False

    def crossover(self,firstGen,secondGen):
        for i in range(1,len(firstGen)):
            if abs(firstGen[i-1] - firstGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
            if abs(secondGen[i-1] - secondGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]

    def mutate(self,gen):
        bound = self.size//2
        from random import randint as rand
        leftSideIndex = rand(0,bound)
        RightSideIndex = rand(bound+1,self.size-1)
        newGen = []
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.size):
            if i not in newGen:
                newGen.append(i)
        gen = newGen
        gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]
        return gen

    def evolve(self):
        for i in range(1,len(self.env),2):
            firstGen = self.env[i-1][:]
            secondGen = self.env[i][:]
            self.crossover(firstGen,secondGen)
            firstGen = self.mutate(firstGen)
            secondGen = self.mutate(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def select(self):
        genUtilities = []
        newEnv = []
        for gen in self.env:
            genUtilities.append(self.fitness(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil = None
        while len(newEnv)<self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])
        return newEnv

    def findInitialSolutions(self):
        for gen in self.env:
            if self.isGoalGen(gen) and gen not in self.solutions:
                print(str(len(self.solutions) + 1) + ". " + str(gen))
                self.solutions.append(gen)

    def geneticAlgorithm(self):
        self.initializeFirstGenereation()
        self.findInitialSolutions()
        while len(self.solutions) < 92: # go through 92 solutions
            self.evolve()
            self.env = self.select()
            if self.goalIndex >= 0:
                try:
                    if self.goal not in self.solutions:
                        print(str(len(self.solutions) + 1) + ". " + str(self.goal))
                        self.solutions.append(self.goal)
                except IndexError:
                    pass
                self.initializeFirstGenereation()
                self.findInitialSolutions()
            else:
                continue
        return self.solutions

solutions = NQueens().geneticAlgorithm()
# print(solutions)