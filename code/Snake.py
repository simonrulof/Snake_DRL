from tkinter import *
from tkinter import ttk
from threading import Thread
import time
import random

import GlobalVar
import Inputs

class Snake:

    def __init__(self, size=760, nbCases = 19):
        self.size = size
        self.nbCases = nbCases
        GlobalVar.gameOver = False
        GlobalVar.leave = False
        GlobalVar.direction = "right"
        GlobalVar.baseDirection = "right"

        self.frameSetup()

        self.createSnake()


    def run(self):
        self.mainLoop()

        self.canvas.create_text(self.size/2, self.size/4, text="Game Over, score : " + str(len(self.snake)) + ", press esc to leave.", font=('Helvetica','20','bold'))
        self.root.update()
        
        while not GlobalVar.leave:
            self.root.update()
            time.sleep(0.1)


        self.root.destroy()
    

    def frameSetup(self):

        self.root = Tk()
        frame = ttk.Frame(self.root)
        self.canvas = Canvas(background="white", width=self.size, height=self.size, highlightthickness=1, highlightbackground="black")
        self.canvas.pack()

        for i in range(self.nbCases - 1):
            self.canvas.create_line((i+1)*self.size/self.nbCases, 0, (i+1)*self.size/self.nbCases, self.size)
            self.canvas.create_line(0, (i+1)*self.size/self.nbCases, self.size, (i+1)*self.size/self.nbCases)


    def generateFruit(self):
        self.positionFruit = (random.randint(0, self.nbCases-1), random.randint(0, self.nbCases-1))
        while self.positionFruit in self.snake:
            self.positionFruit = (random.randint(0, self.nbCases-1), random.randint(0, self.nbCases-1))


    def actualiseCanvas(self, positionLeft : tuple[int, int]):
        size = int(self.canvas['width'])
            
        i, j = positionLeft
        self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="white")

        for (i,j) in self.snake:
            self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="green")
        
        i, j = self.positionFruit
        self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="red")



    """def actualiseCanvas(self):
        size = int(self.canvas['width'])
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                if (i, j) in self.snake:
                    self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="green")

                elif (i, j) == self.positionFruit:
                    self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="red")

                else:
                    self.canvas.create_rectangle(i*size/self.nbCases, j*size/self.nbCases, (i+1)*size/self.nbCases, (j+1)*size/self.nbCases, fill="white")
    """

    def createSnake(self):
        self.snake = [(self.nbCases//2, self.nbCases//2), ((self.nbCases//2) - 1, self.nbCases//2)]
        self.generateFruit()
        
        self.actualiseCanvas((0, 0))


    def actualizeSnake(self):
        newSnake = []
        direct = GlobalVar.direction
        match direct:
            case "right":
                if GlobalVar.baseDirection != "left":
                    newSnake.append((self.snake[0][0] + 1, self.snake[0][1]))
                    GlobalVar.baseDirection = direct
                else:
                    newSnake.append((self.snake[0][0] - 1, self.snake[0][1]))

            case "left":
                if GlobalVar.baseDirection != "right":
                    newSnake.append((self.snake[0][0] - 1, self.snake[0][1]))
                    GlobalVar.baseDirection = direct
                else:
                    newSnake.append((self.snake[0][0] + 1, self.snake[0][1]))
            case "down":
                if GlobalVar.baseDirection != "up":
                    newSnake.append((self.snake[0][0], self.snake[0][1] + 1))
                    GlobalVar.baseDirection = direct
                else:
                    newSnake.append((self.snake[0][0], self.snake[0][1] - 1))
            case "up":
                if GlobalVar.baseDirection != "down":
                    newSnake.append((self.snake[0][0], self.snake[0][1] - 1))
                    GlobalVar.baseDirection = direct
                else:
                    newSnake.append((self.snake[0][0], self.snake[0][1] + 1))


        for position in self.snake[:-1]:
            newSnake.append(position)

        positionLeft = self.snake[-1]

        self.snake = newSnake

        return positionLeft
    

    def checkPosition(self):
        return self.snake[0] == self.positionFruit

    def growSnake(self, positionLeft):
        self.snake.append(positionLeft)

    def checkDeath(self):
        return self.snake[0][0] < 0 or self.snake[0][0] >= self.nbCases or self.snake[0][1] < 0 or self.snake[0][1] >= self.nbCases or self.snake[0] in self.snake[1:]

    def mainLoop(self):
        while not GlobalVar.gameOver and not GlobalVar.leave:
            startTime = time.time()

            
            positionLeft = self.actualizeSnake()

            hasEaten = self.checkPosition()

            if hasEaten:
                self.growSnake(positionLeft)
                self.generateFruit()

            GlobalVar.gameOver = self.checkDeath()

            self.actualiseCanvas(positionLeft)

            self.root.update()
            endTime = time.time()
            while endTime - startTime < 0.2:
                time.sleep(0.01)
                endTime = time.time()



if __name__ == '__main__':
    snake = Snake()
    inputThread = Inputs.Inputs(name="Inputs")
    inputThread.start()
    snake.run()