""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import numpy

import CADrawer
from CA import CA


class CircularCA(CA):
    """A variation of CA that wraps around so that the cells are
    arranged in a ring.
    """
    def __init__(self, rule, n=100, ratio=2):
        """n, m are the number of rows, columns.
        array is the numpy array that contains the data.
        next is the index of the next empty row.
        """
        self.table = self.make_table(rule)
        self.n = n
        # allocate two extra cells for ghosts
        self.m = ratio*n + 1 + 2
        self.array = numpy.zeros((self.n, self.m), dtype=numpy.int8)
        self.next = 0

    def start_single(self):
        """start with one cell in the left of the top row"""
        self.array[0, 1] = 1
        self.next += 1

    def step(self):
        """Executes one time step by computing the next row of the array."""
        i = self.next
        self.next += 1

        a = self.array
        t = self.table

        # copy the ghost cells
        a[i-1,0] = a[i-1,self.m-2]
        a[i-1,self.m-1] = a[i-1,1]

        for j in xrange(1,self.m-1):
            a[i,j] = t[tuple(a[i-1, j-1:j+2])]

    def get_array(self, start=0, end=None):
        """get a slice of columns from the CA, with slice indices
        (start, end).  We need to add one to avoid ghost cells.
        """
        if end==None:
            return self.array[:, start+1:self.m-1]
        else:
            return self.array[:, start+1:end+1]


def main(script, rule=30, n=100, *args):
    rule = int(rule)
    n = int(n)

    ca = CircularCA(rule, n)

    if 'random' in args:
        ca.start_random()
    else:
        ca.start_single()

    ca.loop(n-1)

    if 'eps' in args:
        drawer = CADrawer.EPSDrawer()
    elif 'pil' in args:
        drawer = CADrawer.PILDrawer()
    else:
        drawer = CADrawer.PyplotDrawer()

    if 'trim' in args:
        drawer.draw(ca, start=n/2, end=3*n/2+1)
    else:
        drawer.draw(ca)

    drawer.show()


if __name__ == '__main__':
    import sys
    main(*sys.argv)
