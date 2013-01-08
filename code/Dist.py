
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

import sys
import bisect
import pylab

from Hist import *

class Dist(list):
    """a Dist contains two lists, qs and cs, where qs is a sorted
    list of quantities and cs is the cumulative sum of the frequencies
    of the previous quantities.

    The second list can be converted to percentiles by dividing
    through by self.total(), which returns the total of all the frequencies.

    Note: the cdf makes more sense if the keys in the Dist
    are numeric, but this function works for any data type that
    can be sorted.
    """

    def __init__(self, hist):
        """build the distribution of the quantities in the given Hist
        by sorting the quantities and accumulating the running sum of 
        the frequencies in (runsum)"""
        runsum = Counter()
        self.qs = []
        self.cs = []
        qapp = self.qs.append
        capp = self.cs.append

        # the following list comprehension uses append expressions
        # for their side effect and discards the result.
        [(qapp(q), capp(runsum.incr(f[0])))
         for q, f in sorted(hist.iteritems())]

    def total(self):
        """return the number of quantities in the distribution, which
        is the last value in the cumulative sum"""
        return self.cs[-1]

    def percentile(self, q):
        """return the percentile that corresponds to (q)"""
        if q < self.qs[0]: return 0.0
        if q > self.qs[-1]: return 1.0

        index = bisect.bisect(self.qs, q)
        c = self.cs[index-1]
        return float(c) / self.total()

    def quantile(self, p):
        if p == 0: return self.qs[0]
        if p == 1: return self.qs[-1]

        c = p * self.total()
        index = bisect.bisect(self.cs, c)

        if c == self.cs[index-1]:
            return self.qs[index-1]
        else:
            return self.qs[index]
        return self.qs[index]
        

    def cdf(self):
        """return a tuple of lists, 
        qq: the quantities,
        pp: the percentiles,
        with two elements per quantity."""
        qq = []
        cc = [0]
        [qq.extend((q,q)) for q in self.qs]
        [cc.extend((c,c)) for c in self.cs]
        del cc[-1]

        total = self.total()
        pp = [float(c)/total for c in cc]
        return qq, pp

    def print_cdf(self):
        """print the keys (in increasing order) and the corresponding
        cumulative fractions"""
        qq, pp = self.cdf()
        for q, p in zip(qq, pp):
            print q, p

    def plot_cdf(self, plot_func=pylab.plot, *args, **kwds):
        """plot the cdf as a step function; the optional second
        parameter is one of the line plotting functions in pylab,
        either pylab.plot, pylab.semilogx, pylab.semilogy or pylab.loglog.

        args and kwds are passed along to the plotting function
        """
        qq, pp = self.cdf()
        patches = plot_func(qq, pp, *args, **kwds)
        pylab.xlabel('quantity')
        pylab.ylabel('percentile')
        pylab.title('cdf')

    def plot_ccdf(self, plot_func=pylab.plot, *args, **kwds):
        """plot the complementary cdf; see plot_cdf for parameters
        """
        qq, pp = self.cdf()
        cpp = [1.0 - p for p in pp]
        patches = plot_func(qq, cpp, *args, **kwds)
        pylab.xlabel('quantity')
        pylab.ylabel('complementary cumulative fraction')
        pylab.title('ccdf')

    def show(self):
        pylab.show()

def main(script, filename='', *args):
    h = Hist([1,2,2,4,5])
    d = Dist(h)

    print d.percentile(1.5)
    print d.percentile(2.0)
    print d.percentile(2.5)

    print d.quantile(0.0)
    print d.quantile(0.2)
    print d.quantile(0.25)
    print d.quantile(0.4)
    print d.quantile(0.5)
    print d.quantile(0.6)
    print d.quantile(0.75)
    print d.quantile(0.8)
    print d.quantile(0.9)
    print d.quantile(1.0)

    d.print_cdf()

    #pylab.subplot(1,2,1)
    d.plot_cdf()

    #pylab.subplot(1,2,2)
    #d.plot_ccdf()

    d.show()

if __name__ == '__main__':
    main(*sys.argv)
