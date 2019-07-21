""" Code from Think Complexity, 2nd Edition, by Allen Downey.

Available from http://greenteapress.com

Copyright 2016 Allen B. Downey.
MIT License: https://opensource.org/licenses/MIT
"""

import numpy as np
import matplotlib.pyplot as plt

def make_table(rule):
    """Makes the CA table for a given rule.

    rule: integer 0-255

    returns: NumPy array of uint8
    """
    rule = np.array([rule], dtype=np.uint8)
    table = np.unpackbits(rule)[::-1]
    return table


class Cell1D:
    """Represents a 1-D a cellular automaton"""

    def __init__(self, rule, n, m=None):
        """Initializes the CA.

        rule: integer
        n: number of rows
        m: number of columns

        Attributes:
        table:  rule dictionary that maps from triple to next state.
        array:  the numpy array that contains the data.
        next:   the index of the next empty row.
        """
        self.table = make_table(rule)
        self.n = n
        self.m = 2*n + 1 if m is None else m

        self.array = np.zeros((n, self.m), dtype=np.int8)
        self.next = 0

    def start_single(self):
        """Starts with one cell in the middle of the top row."""
        self.array[0, self.m//2] = 1
        self.next += 1

    def start_random(self):
        """Start with random values in the top row."""
        self.array[0] = np.random.random(self.m).round()
        self.next += 1

    def start_string(self, s):
        """Start with values from a string of 1s and 0s."""
        # TODO: Check string length
        self.array[0] = np.array([int(x) for x in s])
        self.next += 1

    def loop(self, steps=1):
        """Executes the given number of time steps."""
        for i in range(steps):
            self.step()

    def step(self):
        """Executes one time step by computing the next row of the array."""
        a = self.array
        i = self.next
        window = [4, 2, 1]
        c = np.correlate(a[i-1], window, mode='same')
        a[i] = self.table[c]
        self.next += 1

    def get_array(self, start=0, end=None):
        """Gets a slice of columns from the CA.

        Avoids copying if possible.

        start: index of first column
        end: index of the last column plus one
        """
        # TODO: Not sure it makes sense to make selecting the
        # whole array into a special case.
        if start==0 and end==None:
            return self.array
        else:
            return self.array[:, start:end]


class Wrap1D(Cell1D):
    """Implements a 1D cellular automaton with wrapping."""

    def step(self):
        # perform the usual step operation
        Cell1D.step(self)

        # fix the first and last cells by copying from the other end
        i = self.next-1
        row = self.array[i]
        row[0], row[-1] = row[-2], row[1]


class Cell1DViewer:
    """Draws a CA object using matplotlib."""

    cmap = plt.get_cmap('Blues')
    options = dict(alpha=0.7, interpolation='none')

    def __init__(self, ca):
        self.ca = ca

    def draw(self, start=0, end=None):
        """Draws the CA using pyplot.imshow.

        start: index of the first column to be shown
        end: index of the last column to be shown
        """
        a = self.ca.get_array(start, end)
        n, m = a.shape
        plt.axis([0, m, 0, n])
        plt.xticks([])
        plt.yticks([])

        self.options['extent'] = [0, m, 0, n]
        plt.imshow(a, cmap=self.cmap, **self.options)


def print_table(table):
    """Prints the rule table in LaTeX format."""
    print('\\beforefig')
    print('\\centerline{')
    print('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}')
    print('\\hline')

    res = ['prev'] + ['{0:03b}'.format(i) for i in range(8)]
    print(' & '.join(res) + ' \\\\ \n\\hline')

    res = ['next'] + [str(x) for x in table]
    print(' &   '.join(res) + ' \\\\ \n\\hline')

    print('\\end{tabular}}')


class EPSDrawer:
    """Draw a CA using encapsulated Postscript (EPS)."""

    def draw(self, ca, start=0, end=None):
        """Draws the CA using pyplot.pcolor.

        start: index of the first column to be shown
        end: index of the last column to be shown
        """
        a = ca.get_array(start, end)
        self.n, self.m = a.shape

        self.cells = []
        for i in xrange(self.n):
            for j in xrange(self.m):
                if a[i, j]:
                    self.cells.append((i, j))

    def save(self, filename='ca.eps'):
        """Saves the representation of the CA.

        filename: string
        """
        with open(filename, 'w') as fp:
            self.print_header(fp)
            self.print_outline(fp)
            self.print_cells(fp)
            self.print_footer(fp)

    def print_header(self, fp, size=0.9, border=2):
        """Writes the EPS header and defines /c."""
        fp.write('%!PS-Adobe-3.0 EPSF-3.0\n')
        fp.write('%%%%BoundingBox: %d %d %d %d\n' %
                 (border, border, self.m+border, self.n+border))

        fp.write('1 -1 scale\n')
        fp.write('0 %d translate\n' % -self.n)
        fp.write('/c {\n')
        fp.write('   newpath moveto\n')
        fp.write('   0 %g rlineto\n' % size)
        fp.write('   %g 0 rlineto\n' % size)
        fp.write('   0 -%g rlineto\n' % size)
        fp.write('   closepath fill\n')
        fp.write('} def\n')

    def print_outline(self, fp):
        """Writes the code that draws the outline."""
        fp.write('newpath 0.1 setlinewidth 0 0 moveto\n')
        fp.write('0 %d rlineto\n' % self.n)
        fp.write('%d 0 rlineto\n' % self.m)
        fp.write('0 -%d rlineto\n' % self.n)
        fp.write('closepath stroke\n')

    def print_cells(self, fp):
        """Writes the code that draws the cells."""
        for i, j in self.cells:
            fp.write('%d %d c\n' % (j, i))

    def print_footer(self, fp):
        """Writes the footer code."""
        fp.write('%%EOF\n')
