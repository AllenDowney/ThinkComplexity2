""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import matplotlib.pyplot as pyplot
import numpy

from CA import CA
import CADrawer


def fit_loglog(xs, ys, start=0):
    """Computes the slope and intercept of log(number of boxes)
    vs. log(1/epsilon), where epsilon is the size of the boxes.

    See http://en.wikipedia.org/wiki/Box-counting_dimension
    """
    coefs = numpy.polyfit(numpy.log(xs[start:]), 
                          numpy.log(ys[start:]),
                          1)
    return coefs


def plot_loglog(ts, ys, filename=None):
    """Makes a log-log plot showing number of boxes vs 1/epsilon,
    where epsilon is the size of the boxes.

    See http://en.wikipedia.org/wiki/Box-counting_dimension
    """
    pyplot.clf()
    pyplot.plot(ts, ys, linewidth=2)
    pyplot.xscale('log')
    pyplot.yscale('log')
    pyplot.title('Box counting dimension')
    pyplot.xlabel(r'$1/\varepsilon$')
    pyplot.ylabel(r'$N(\varepsilon)$')
    
    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()


def count(ca):
    """Computes the cumulative sum of the number of "on" cells in a CA
    
    Returns (ts, ys) where ts is the timesteps and ys is the cumsum.
    """
    ts = range(1, ca.n+1)
    ys = numpy.cumsum([numpy.sum(ca.array[i, :]) for i in xrange(ca.n)])
    return ts, ys


def save_ca(ca, filename):
    """Draws the CA and saves it in an EPS file."""
    drawer = CADrawer.EPSDrawer()
    pyplot.clf()
    drawer.draw(ca)
    drawer.save(filename)


def fractal_dimension(rule=18, n=512, save=False):
    """Estimates the fractal dimension for a given rule and number of steps.
    """
    ca = CA(rule, n)
    ca.start_single()
    ca.loop(n-1)

    if save:
        filename = 'fractal-%d-%d.eps' % (rule, n)
        print 'Writing', filename
        save_ca(ca, filename)

    ts, ys = count(ca)
    if save:
        filename = 'fractal_dim-%d-%d.pdf' % (rule, n)
        print 'Writing', filename
        plot_loglog(ts, ys, filename)

    slope, inter = fit_loglog(ts, ys, n/2)
    return slope


def main(script):

    print 254, fractal_dimension(254, 4, True)
    print 254, fractal_dimension(254, 8, True)
    print 18, fractal_dimension(18, 64, True)

    print 1, fractal_dimension(1, 128)
    
    print 30, fractal_dimension(30, 16)
    print 30, fractal_dimension(30, 32)
    print 30, fractal_dimension(30, 64)
    print 30, fractal_dimension(30, 128)

    print 89, fractal_dimension(30, 64)

    for i in range(256):
        print i, fractal_dimension(i, 16, False)


    

if __name__ == '__main__':
    import sys
    main(*sys.argv)
