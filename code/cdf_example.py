""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import sys

import matplotlib.pyplot as pyplot

import Cdf

def plot_ranks(hist, scale='log'):
    """Plots frequency vs. rank."""
    t = rank_freq(hist)
    rs, fs = zip(*t)

    pyplot.clf()
    pyplot.xscale(scale)
    pyplot.yscale(scale)
    pyplot.title('Zipf plot')
    pyplot.xlabel('rank')
    pyplot.ylabel('frequency')
    pyplot.plot(rs, fs, 'r-')
    pyplot.show()


def main(name, *args):
    import Cdf
    cdf = Cdf.MakeCdfFromList([1,2,2,4,5])
    prob = cdf.Prob(2)
    print prob
    value = cdf.Value(0.5)
    print value

    xs, ps = cdf.Render()
    for x, p in zip(xs, ps):
        print x, p

    pyplot.plot(xs, ps, linewidth=3)
    pyplot.axis([0.9, 5.1, 0, 1])
    pyplot.title('CDF')
    pyplot.xlabel('value, x')
    pyplot.ylabel('probability, cdf(x)')
    #pyplot.show()

    pyplot.savefig('cdf_example.eps')
    pyplot.savefig('cdf_example.pdf')

if __name__ == '__main__':
    main(*sys.argv)
