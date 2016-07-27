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
from matplotlib.patches import RegularPolygon

from collections import namedtuple

"""
For animation to work, you might have to install
ffmpeg.  On Ubuntu and Linux Mint, the following should work.

    sudo add-apt-repository ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get install ffmpeg
"""

class Turmite:
    """Implements Langton's Ant"""

    # map from orientation to (di, dj)
    move = { 0: (-1, 0),  # north
             1: (0, 1),   # east
             2: (1, 0),   # south
             3: (0, -1) } # west

    def __init__(self, n, m=None):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        """
        m = n if m is None else m
        self.n = n
        self.m = m
        self.array = np.zeros((n, m), np.uint8)
        self.loc = (n//2, m//2)
        self.state = 0

    def step(self):
        """Executes one time step."""
        try:
            cell = self.array[self.loc]
        except IndexError:
            sys.exit()

        # toggle the current cell
        self.array[self.loc] ^= 1
        
        if cell:
            # turn left
            self.state = (self.state + 3) % 4
        else:
            # turn right
            self.state = (self.state + 1) % 4

        move = self.move[self.state]
        self.loc = self.loc[0] + move[0], self.loc[1] + move[1]


class TurmiteViewer:
    """Generates an animated view of the grid."""

    cmap = plt.get_cmap('Oranges')

    def __init__(self, turmite):
        self.turmite = turmite
        self.im = None
        self.arrow = None
        self.hlines = None
        self.vlines = None

    def draw(self, grid=False):
        """Updates the display with the state of the grid."""
        self.draw_array()
        self.draw_arrow()
        if grid:
            self.draw_grid()

    def draw_array(self):
        """Draws the cells."""
        a = self.turmite.array
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
        n, m = self.turmite.n, self.turmite.m
        lw = 2 if m < 10 else 1
        options = dict(color='white', linewidth=lw)

        rows = np.arange(1, n)
        self.hlines = plt.hlines(rows, 0, m, **options)
        
        cols = np.arange(1, m)
        self.vlines = plt.vlines(cols, 0, n, **options)

    def draw_arrow(self):
        """Draws the arrow."""
        center, angle = self.arrow_specs()
        self.arrow = RegularPolygon(center, 3, color='orange', 
                                        radius=0.4, orientation=angle)
        ax = plt.gca()
        ax.add_patch(self.arrow)

    def arrow_specs(self):
        """Computes the center and orientation of the arrow."""
        n = self.turmite.n
        i, j = self.turmite.loc
        center = j+0.5, n-i-0.5
        angle = -np.pi / 2 * self.turmite.state
        return center, angle

    def animate(self, frames=20, interval=200, grid=False):
        """Creates an animation.
        
        frames: number of frames to draw
        interval: time between frames in ms
        """
        fig = plt.gcf()
        self.draw(grid)
        anim = animation.FuncAnimation(fig, self.animate_func,
                                       init_func=self.init_func,
                                       frames=frames, interval=interval,
                                       repeat=False)
        return anim

    def init_func(self):
        """Called at the beginning of an animation."""
        pass

    def animate_func(self, i):
        """Draws one frame of the animation."""
        self.turmite.step()

        # update the array
        a = self.turmite.array
        self.im.set_array(a)

        # update the arrow
        center, angle = self.arrow_specs()
        self.arrow.xy = center
        self.arrow.orientation = angle

        return (self.im, self.arrow)


def main(script, *args):
    """Runs Langton's Ant."""
    n, m = 70, 80
    turmite = Turmite(n, m)
    viewer = TurmiteViewer(turmite)

    # run a few steps and draw the end condition
    #for i in range(5):
    #    turmite.step()
    #viewer.draw(grid=True)

    # run a short animation
    #anim = viewer.animate(frames=5, interval=1000, grid=True)

    anim = viewer.animate(frames=10700, interval=0)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main(*sys.argv)


