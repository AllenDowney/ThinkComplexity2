""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""
import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import RegularPolygon

from Cell2D import Cell2D
from animate import animate


class Turmite(Cell2D):
    """Implements Langton's Ant"""

    # map from orientation to (di, dj)
    move = {0: (-1, 0),  # north
            1: (0, 1),   # east
            2: (1, 0),   # south
            3: (0, -1)}  # west

    def __init__(self, n, m=None):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        """
        m = n if m is None else m
        self.array = np.zeros((n, m), np.uint8)
        self.loc = np.array([n//2, m//2])
        self.state = 0

    def step(self):
        """Executes one time step."""
        # in order to use an array as an index, we have to make it a tuple
        loc = tuple(self.loc)

        # get the state of the current cell
        try:
            cell = self.array[loc]
        except IndexError:
            raise IndexError('The turmite has gone off the grid')

        # toggle the current cell
        self.array[loc] ^= 1

        if cell:
            # turn left
            self.state = (self.state + 3) % 4
        else:
            # turn right
            self.state = (self.state + 1) % 4

        move = self.move[self.state]
        self.loc += move

    def draw(self):
        """Updates the display with the state of the grid."""
        super().draw(cmap='Oranges')

        # draw the arrow
        center, orientation = self.arrow_specs()
        self.arrow = RegularPolygon(center, 3, color='orange',
                                    radius=0.4, orientation=orientation)
        ax = plt.gca()
        ax.add_patch(self.arrow)

    def arrow_specs(self):
        """Computes the center and orientation of the arrow."""
        a = self.array
        n, m = a.shape
        i, j = self.loc
        center = j+0.5, n-i-0.5
        orientation = -np.pi / 2 * self.state
        return center, orientation


def main(script, *args):
    """Runs Langton's Ant."""
    n, m = 70, 80
    turmite = Turmite(n, m)
    anim = animate(turmite, frames=10700, interval=0)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main(*sys.argv)
