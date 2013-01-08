import sys
import string
from math import *

class Hist(dict):
    """a histogram is a dictionary that maps from each key (x) to the
    number of times the key has appeared (frequency, f)
    """
    
    def __init__(self, seq=[]):
        "create a new histogram starting with the items in seq"
        for x in seq:
            self.count(x)

    def count(self, x):
        "increment the counter associated with key x"
        self[x] = self.get(x, 0) + 1

    def pdf(self):
        """return a list of tuples where each tuple is a key x
        and a frequency f.
        """
        # sort the x,f pairs in the dictionary by x
        t = self.items()
        t.sort()
        return t
        
    def cdf(self):
        """return a list of tuples where each tuple is a key x
        and the cumulative fraction of keys less than or equal
        to x.  This is the empirical CDF of the keys in the Hist.

        Note: the cdf makes more sense if the keys in the Hist
        are numeric, but this function works for any data type that
        can be sorted.
        """
        # accumulate the running sum of the frequencies and
        # the fraction of the total (percentile)
        total = sum(self.itervalues())
        runsum = 0
        cdf = []
        
        for x, f in self.pdf():
            runsum += f
            percentile = float(runsum) / total
            cdf.append((x, percentile))
        return cdf
    
    def rank_freq(self):
        """return a list of tuples where each tuple is a rank
        and the number of times the key with that rank appeared.
        """
        # sort the list of frequency-value pairs
        t = [f for f in self.itervalues()]
        t.sort()
        t.reverse()

        # enumerate the frequencies in decreasing order
        rf = [(r+1, f) for r, f in enumerate(t)]
        return rf


class Zipf(Hist):
    """Zipf is a histogram that maps from words to frequencies.

    It provides methods to print data for a Zipf plot (frequency
    versus rank) and a complementary CDF (percentile versus key),
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
        """print the data for the rank-frequency plot described below        
        """
        for r, f in self.rank_freq():
            print log10(r), log10(f)

    def make_hist(self):
        """make a histogram of the frequencies in this Zipf object"""
        freqs = self.itervalues()
        hist = Hist(freqs)
        return hist
        
    def print_ccdf(self):
        """print the data for a ccdf (complementary cumulative
        distribution function) of the frequencies.  WARNING: this
        function might make your head hurt because the frequencies
        from the Zipf object are the keys in hist.
        """
        # print the complementary cdf on a log-log scale
        for x, p in self.make_hist().cdf():
            if p==1.0: break
            print log10(x), log10(1-p)

    def print_pdf(self):
        """print the data for a pdf of the frequencies
        """
        # print the (unnormalized) pdf on a log-log scale
        for x, f in self.make_hist().pdf():
            print log10(x), log10(f)

def main(name, filename='', flag=None, *args):
    z = Zipf()
    z.process_file(filename)
    if flag == None:
        z.print_ranks()
    else:
        if flag == 'ccdf':
            z.print_ccdf()
        elif flag == 'pdf':
            z.print_pdf()

if __name__ == '__main__':
    main(*sys.argv)
