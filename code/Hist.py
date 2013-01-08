
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

import sys

class Counter(list):
    """a Counter encapsulates a singleton list.  It is useful for
    replacing arithmetic operations with method invocations, which
    can make it easier to replace a loop with a list comprehension"""

    def __init__(self, start=0):
        """initialize the counter with the given starting value"""
        list.__init__(self, [start])

    def incr(self, amount=1):
        """increment the counter by the given amount and return
        the new value"""
        self[0] += amount
        return self[0]


class Hist(dict):
    """a Hist is a dictionary that maps from each quantity (q) to a Counter
    that counts the number of times the quantity has appeared (frequency)
    """

    def __init__(self, seq=[]):
        "create a new histogram starting with the quantities in (seq)"
        self.count_seq(seq)

    def count_seq(self, seq):
        """add the elements of (seq) to the histogram"""
        setd = self.setdefault
        [setd(q, Counter()).incr() for q in seq]

    def count(self, q):
        "increment the counter associated with quantity (q)"
        self.setdefault(q, Counter()).incr()

    def print_most_frequent(self, n=None):
        """print the (n) most frequent quantities and their frequencies;
        if (n) is omitted or None, print all
        """
        t = [(f[0], q) for q, f in self.iteritems()]
        t.sort(reverse=True)
        for f, q in t[0:n]:
            print q, f


def main(script, *args):
    seq = [1,2,2,4,5]
    h = Hist(seq)
    h.count(5)
    print h

    h.print_most_frequent(3)

if __name__ == '__main__':
    main(*sys.argv)
