""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""
from __future__ import print_function, division

import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from scipy.signal import convolve2d

"""
For animation to work in the notebook, you might have to install
ffmpeg.  On Ubuntu and Linux Mint, the following should work.

    sudo add-apt-repository ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get install ffmpeg
"""

class Life:
    """Implements Conway's Game of Life."""

    kernel = np.array([[1, 1, 1],
                       [1,10, 1],
                       [1, 1, 1]])

    table = np.zeros(20, dtype=np.uint8)
    table[[3, 12, 13]] = 1

    def __init__(self, n, m=None):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        """
        m = n if m is None else m
        self.array = np.zeros((n, m), np.uint8)

    def add_cells(self, row, col, *strings):
        """Adds cells at the given location.

        row: top row index
        col: left col index
        strings: list of strings of 0s and 1s
        """
        for i, s in enumerate(strings):
            self.array[row+i, col:col+len(s)] = np.array([int(b) for b in s])

    def step(self):
        """Executes one time step."""
        c = convolve2d(self.array, self.kernel, mode='same')
        self.array = self.table[c]


class LifeViewer:
    """Generates an animated view of an array image."""

    cmap = plt.get_cmap('Greens')

    def __init__(self, viewee):
        self.viewee = viewee
        self.im = None
        self.hlines = None
        self.vlines = None

    def step(self):
        """Advances the viewee one step."""
        self.viewee.step()

    def draw(self, grid=False):
        """Updates the display with the state of the grid."""
        self.draw_array()
        if grid:
            self.draw_grid()

    def draw_array(self):
        """Draws the cells."""
        a = self.viewee.array
        n, m = a.shape
        plt.axis([0, m, 0, n])
        plt.xticks([])
        plt.yticks([])

        self.im = plt.imshow(a, cmap=self.cmap,
                             interpolation='none',
                             vmin=0, vmax=1,
                             extent=[0, m, 0, n])

    def draw_grid(self):
        """Draws the grid."""
        a = self.viewee.array
        n, m = a.shape
        lw = 2 if m < 10 else 1
        options = dict(color='white', linewidth=lw)

        rows = np.arange(1, n)
        self.hlines = plt.hlines(rows, 0, m, **options)

        cols = np.arange(1, m)
        self.vlines = plt.vlines(cols, 0, n, **options)

    def animate(self, frames=20, interval=200, grid=False):
        """Creates an animation.

        frames: number of frames to draw
        interval: time between frames in ms
        """
        fig = plt.figure()
        self.draw(grid)
        anim = animation.FuncAnimation(fig, self.animate_func,
                                       init_func=self.init_func,
                                       frames=frames, interval=interval)
        return anim

    def init_func(self):
        """Called at the beginning of an animation."""
        pass

    def animate_func(self, i):
        """Draws one frame of the animation."""
        self.viewee.step()
        a = self.viewee.array
        self.im.set_array(a)
        return (self.im,)


def main(script, *args):
    """Constructs a puffer train.

    Uses the entities in this file:
    http://www.radicaleye.com/lifepage/patterns/puftrain.lif
    """

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

    n = 400
    m = 600
    life = Life(n, m)
    col = 120
    life.add_cells(n//2+12, col, *lwss)
    life.add_cells(n//2+26, col, *lwss)
    life.add_cells(n//2+19, col, *bhep)
    viewer = LifeViewer(life)
    anim = viewer.animate(frames=100, interval=0)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main(*sys.argv)


