""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import sys
import string

import matplotlib.pyplot as pyplot

import Pmf


def rank_freq(hist):
    """Returns a list of tuples where each tuple is a rank
    and the number of times the item with that rank appeared.
    """
    # sort the list of frequencies in decreasing order
    freqs = hist.Freqs()
    freqs.sort(reverse=True)

    # enumerate the ranks and frequencies 
    rf = [(r+1, f) for r, f in enumerate(freqs)]
    return rf


def print_ranks(hist):
    """Prints the rank vs. frequency data."""
    for r, f in rank_freq(hist):
        print r, f


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


def iter_words(filename):
    """A generator that yields the words from a file one at a time,
    with the punctuation stripped."""
    fp = open(filename, 'r')
    for line in fp:
        line = line.replace('--', ' ')
        line = line.replace("'s ", ' ')
        for word in line.rstrip().split():
            word = word.strip(string.punctuation)
            yield word


def main(name, filename='gatsby.txt', flag='print', *args):

    # build a Zipf histogram of the words in filename
    iter = iter_words(filename)
    hist = Pmf.MakeHistFromList(iter)

    # either print the results or plot them
    if flag == 'print':
        print_ranks(hist)
    elif flag == 'plot':
        plot_ranks(hist)
    else:
        print 'Usage: Zipf.py filename [print|plot]'


if __name__ == '__main__':
    main(*sys.argv)
