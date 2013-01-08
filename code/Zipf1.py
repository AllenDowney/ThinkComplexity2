import sys
import string
from math import *

class Hist(dict):
    """a histogram is a dictionary that maps from each item (x) to the
    number of times the item has appeared (frequency, f)
    """
    
    def __init__(self, seq=[]):
        "create a new histogram starting with the items in seq"
        for x in seq:
            self.count(x)

    def count(self, x):
        "increment the counter associated with item x"
        self[x] = self.get(x, 0) + 1

    def pdf(self):
        """return a list of tuples where each tuple is a value x
        and a frequency f.
        """
        return []
        
    def cdf(self):
        """return a list of tuples where each tuple is a value x
        and the cumulative fraction of values less than or equal
        to x.  This is the empirical CDF of the values in the Hist.

        Note: the cdf makes more sense if the data values in the Hist
        are numeric, but this function works for any data type that
        can be sorted.
        """
        return []
    
    def rank_freq(self):
        """return a list of tuples where each tuple is a rank
        and the number of times the item with that rank appeared.
        """
        return []


class Zipf(Hist):
    """Zipf is a histogram that maps from words to frequencies.

    It provides methods to print data for a Zipf plot (frequency
    versus rank) and a complementary CDF (percentile versus value),
    both on log-log axes. 
    """
    def process_file(self, filename):

        fp = open(filename, 'r')
        for line in fp:
            line = line.replace('--', ' ')
            line = line.replace("'s ", ' ')
            for word in line.rstrip().split():
                self.process_word(word)

    def process_word(self, word):
        word = word.strip(string.punctuation)
        self.count(word)

    def print_ranks(self):
        """print the data for a bar chart in which the x-axis
        shows ranks in increasing order and the y-axis shows the
        frequency of the value with the given rank.
        """
        for r, f in self.rank_freq():
            print log10(r), log10(f)


def main(name, filename='', flag=None, *args):
    z = Zipf()
    z.process_file(filename)
    z.print_ranks()

if __name__ == '__main__':
    main(*sys.argv)
