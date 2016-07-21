""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy.signal import convolve2d


class Life(object):
    """Implements Conway's Game of Life.

    n:     the number of rows and columns
    """
    table = np.zeros(20, dtype=np.uint8)
    table[[3, 12, 13]] = 1

    def __init__(self, n, m=None):
        """Attributes:
        n:      number of rows and columns
        """
        self.n = n
        self.m = n if m is None else m
        self.array = np.zeros((n, m), np.uint8)
        self.kernel = np.array([[1, 1, 1],
                                   [1,10, 1],
                                   [1, 1, 1]])

    def add_cells(self, x, y, *strings):
        """Adds cells at the given location.
        
        x: left coordinate
        y: top coordinate
        strings: list of strings of 0s and 1s
        """
        for i, s in enumerate(strings):
            self.array[y+i, x:x+len(s)] = np.array([int(b) for b in s])

    def step(self):
        """Executes one time step."""
        c = convolve2d(self.array, self.kernel, mode='same')
        self.array = self.table[c]


class LifeViewer:
    """Generates an animated view of the grid."""
    def __init__(self, life):
        self.life = life
        self.im = None
    
    def draw(self):
        """Updates the display with the state of the grid."""
        a = self.life.array
        cmap = plt.get_cmap('Greens')
        self.im = plt.imshow(a, cmap=cmap, interpolation='none')
        plt.xticks([])
        plt.yticks([])

    def animate(self, frames=20, interval=200):
        """Creates an animation.
        
        frames: number of frames to draw
        interval: time between frames in ms
        """
        fig = plt.figure()
        self.draw()
        anim = animation.FuncAnimation(fig, self.animate_func, 
                                       frames=frames, interval=interval)
        return anim

    def animate_func(self, i):
        """Draws one frame of the animation."""
        if i > 0:
            self.life.step()
        a = self.life.array
        self.im.set_array(a)
        return (self.im,)

glider_gun = [
    '000000000000000000000000100000000000',
    '000000000000000000000010100000000000',
    '000000000000110000001100000000000011',
    '000000000001000100001100000000000011',
    '110000000010000010001100000000000000',
    '110000000010001011000010100000000000',
    '000000000010000010000000100000000000',
    '000000000001000100000000000000000000',
    '000000000000110000000000000000000000'
]

lwss = [
    '0001',
    '00001',
    '10001',
    '01111'
]

bhep = [
    '1',
    '011',
    '001',
    '001',
    '01'
]

def main(script, *args):
    n = 200
    m = 1200
    life = Life(n, m)
    #life.add_cells(n//2, n//2, '11101', '1', '00011', '01101', '10101')
    #life.add_cells(n//2, n//2, *glider_gun)
    x = 100
    life.add_cells(x, n//2-8, *lwss)
    life.add_cells(x, n//2+6, *lwss)
    life.add_cells(x, n//2-1, *bhep)
    viewer = LifeViewer(life)
    #viewer.draw()
    anim = viewer.animate(frames=100, interval=0)
    plt.show()

if __name__ == '__main__':
    main(*sys.argv)


