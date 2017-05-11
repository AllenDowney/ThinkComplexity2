""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""
from __future__ import print_function, division

import sys
import matplotlib.pyplot as plt

from Life import Life, LifeViewer


def main(script, *args):
    """Constructs the rabbits methusela.

    http://www.argentum.freeserve.co.uk/lex_r.htm#rabbits
    """

    rabbits = [
        '1000111',
        '111001',
        '01'
    ]

    n = 400
    m = 600
    life = Life(n, m)
    life.add_cells(n//2, m//2, *rabbits)
    viewer = LifeViewer(life)
    anim = viewer.animate(frames=100, interval=1)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main(*sys.argv)
