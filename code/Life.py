""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""
import sys

import numpy as np
import matplotlib.pyplot as plt

from Cell2D import Cell2D
from animate import animate
from scipy.signal import correlate2d


class Life(Cell2D):
    """Implementation of Conway's Game of Life."""
    kernel = np.array([[1, 1, 1],
                       [1,10, 1],
                       [1, 1, 1]])

    table = np.zeros(20, dtype=np.uint8)
    table[[3, 12, 13]] = 1

    def step(self):
        """Executes one time step."""
        c = correlate2d(self.array, self.kernel, mode='same')
        self.array = self.table[c]


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
    anim = animate(life)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main(*sys.argv)
