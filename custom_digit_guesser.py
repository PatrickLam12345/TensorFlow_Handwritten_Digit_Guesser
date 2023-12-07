import pygame
import tensorflow as tf
import numpy as np
from tkinter import *
from tkinter import messagebox

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.neighbors = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x * 20, self.y * 20, 20, 20))
    
    def generateNeighbors(self, g):
        r = self.x
        c = self.y

        if r > 0:
            self.neighbors.append(g.pixels[r-1][c])
        if c > 0:
            self.neighbors.append(g.pixels[r][c-1])
        if r < 28 - 1:
            self.neighbors.append(g.pixels[r+1][c])
        if c < 28 - 1:
            self.neighbors.append(g.pixels[r][c+1])

        if r > 0 and c > 0:
            self.neighbors.append(g.pixels[r-1][c-1])
        if r < 28 - 1 and c > 0:
            self.neighbors.append(g.pixels[r+1][c-1])
        if r < 28 - 1 and c < 28 - 1:
            self.neighbors.append(g.pixels[r+1][c+1])
        if r > 0 and c < 28 - 1:
            self.neighbors.append(g.pixels[r-1][c+1])

class Grid:
    def __init__(self):
        self.generatePixels()
    
    def generatePixels(self):
        self.pixels = []
        for r in range(28):
            self.pixels.append([])
            for c in range(28):
                self.pixels[r].append(Pixel(r, c))

        for r in range(28):
            for c in range(28):
                self.pixels[r][c].generateNeighbors(self)
    
    def clicked(self, pos):
        r = pos[0] // 20
        c = pos[1] // 20
        return self.pixels[r][c]

    def draw(self, surface):
        for r in self.pixels:
            for c in r:
                c.draw(surface) # c is Pixel

    def convert_binary(self):
        matrix = []
        for r in range(28):
            matrix.append([])
            for c in range(28):
                if self.pixels[r][c].color == (0, 0, 0):
                    matrix[r].append(1)
                else:
                    matrix[r].append(0)
                    
        return([matrix])

        
def guess_digit(img):
    model = tf.keras.models.load_model("digit_guesser_model")
    predictions = model.predict(img)
    print(predictions)
    digit_guessed = (np.argmax(predictions[0]))
    print(f"I predict this number is a: {digit_guessed}")
    window = Tk()
    window.withdraw()
    messagebox.showinfo(f"Prediction: 'I predict this number is a: {digit_guessed}'")
    window.destroy()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                preprocessed_image = g.convert_binary()
                guess_digit(preprocessed_image)
                g.generatePixels()
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)    
                clicked.color = (0, 0, 0)
                for neighbor in clicked.neighbors:
                    neighbor.color = (0, 0, 0)

        g.draw(screen)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((560, 560))
pygame.display.set_caption("Number Guesser")
g = Grid()
main()

pygame.quit()