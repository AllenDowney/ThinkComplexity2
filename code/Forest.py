""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import numpy
import scipy.ndimage

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot

import fractal


def vfunc(con, rand, p=0.05, f=0.005):
    """Computes an update in the forest fire model.

    con: an element from the convolution array
    rand: an element from a random array

    The output is 0 for an empty cell, 1 for a tree, and 10 for
    a burning tree.
    """
    # tree + neighbor on fire = burning
    if con >= 110:
        return 10

    # no tree, check for a new tree
    if con < 100:
        if rand < p:
            return 1
        else:
            return 0
    
    # otherwise, tree + no neighbor on fire, check spark
    if rand < f:
        return 10
    else:
        return 1

update_func = numpy.vectorize(vfunc, [numpy.int8])


class Forest(object):
    """Implements the Bak-Chen-Tang forest fire model.

    n:     the number of rows and columns
    """

    def __init__(self, n, mode='wrap'):
        """Attributes:
        n:      number of rows and columns
        mode:   how border conditions are handled
        array:  the numpy array that contains the data.
        weights: the kernel used for convolution
        """
        self.n = n
        self.mode = mode
        self.array = numpy.zeros((n, n), numpy.int8)
        self.weights = numpy.array([[1,1,1],
                                    [1,100,1],
                                    [1,1,1]])

    def get_array(self, start=0, end=None):
        """Gets a slice of columns from the CA, with slice indices
        (start, end).  Avoid copying if possible.
        """
        if start==0 and end==None:
            return self.array
        else:
            return self.array[:, start:end]

    def loop(self, steps=1):
        """Executes the given number of time steps."""
        [self.step() for i in xrange(steps)]

    def step(self):
        """Executes one time step."""
        con = scipy.ndimage.filters.convolve(self.array, 
                                             self.weights,
                                             mode=self.mode)
        rand = numpy.random.rand(self.n, self.n)
        self.array = update_func(con, rand)

    def count(self):
        data = []
        a = numpy.int8(self.array == 1)
        for i in range(self.n):
            total = numpy.sum(a[:i, :i])
            data.append((i+1, total))
        return zip(*data)


class ForestViewer(object):
    """Generates an animated view of the forest."""
    def __init__(self, forest, cmap=matplotlib.cm.gray_r):
        self.forest = forest
        self.cmap = cmap

        self.fig = pyplot.figure()
        pyplot.axis([0, forest.n, 0, forest.n])
        pyplot.xticks([])
        pyplot.yticks([])

        self.pcolor = None
        self.update()

    def update(self):
        """Updates the display with the state of the forest."""
        if self.pcolor:
            self.pcolor.remove()

        a = self.forest.array
        self.pcolor = pyplot.pcolor(a, vmax=10, cmap=self.cmap)
        self.fig.canvas.draw()

    def animate(self, steps=10):
        """Creates the GUI and then invokes animate_callback.

        Generates an animation with the given number of steps.
        """
        self.steps = steps
        self.fig.canvas.manager.window.after(1000, self.animate_callback)
        pyplot.show()

    def animate_callback(self):
        """Runs the animation."""
        for i in range(self.steps):
            self.forest.step()
            self.update()


def main(script, n=50, steps=50, *args):

    n = int(n)
    steps = int(steps)

    forest = Forest(n)

    for i in range(steps):
        forest.step()
        xs, ys = forest.count()

        slope, inter = fractal.fit_loglog(xs, ys, n/4)
        print i+1, slope

    fractal.plot_loglog(xs, ys)    

    import CADrawer
    drawer = CADrawer.EPSDrawer()
    drawer.draw(forest)
    drawer.save('forest.eps')

if __name__ == '__main__':
    import sys

    profile = False
    if profile:
        import cProfile
        cProfile.run('main(*sys.argv)')
    else:
        main(*sys.argv)
