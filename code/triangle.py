"""Solution to a brain teaser at http://projecteuler.net/problem=67

Author: Allen B. Downey
Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

import operator
import os

def read_file(filename='triangle.txt'):
    ts = []
    for line in open(filename):
        t = line.strip().split()
        t = [int(x) for x in t]
        ts.append(t)
    return ts

def max_path(ts):
    cache = {}

    def max_subpath(i, j):
        try:
            return cache[i,j]
        except KeyError:
            pass

        root = ts[i][j]
        res = root + max(max_subpath(i+1, j), max_subpath(i+1, j+1))

        cache[i,j] = res
        return res

    n = len(ts)
    for i in xrange(n):
        cache[n-1, i] = ts[n-1][i]

    return max_subpath(0, 0)
        
def max_path2(ts):
    n = len(ts)
    for i in xrange(n-2, -1, -1):
        for j in xrange(0, i+1):
            ts[i][j] += max(ts[i+1][j], ts[i+1][j+1])
    return ts[0][0]

def max_path3(ts):
    [operator.setitem(ts[i], j, ts[i][j] + max(ts[i+1][j], ts[i+1][j+1]))
     for i in xrange(len(ts)-2, -1, -1)
         for j in xrange(0, i+1)]
    return ts[0][0]

def etime():
    """see how much user and system time this process has used
    so far and return the sum"""
    user, sys, chuser, chsys, real = os.times()
    return user+sys

def timeit(func, ts):
    start = etime()
    print func(ts)
    end = etime()
    print end-start

ts = read_file()

timeit(max_path, ts)
timeit(max_path2, ts)

ts = read_file()
timeit(max_path3, ts)
