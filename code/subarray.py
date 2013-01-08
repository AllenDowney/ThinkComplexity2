"""Solution to maximum subarray problem.

Author: Allen B. Downey
Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

cache = {}

def sum_subarray(t, i, n):
    """Find the total of elements i through i+n."""
    try:
        return cache[i, n]
    except KeyError:
        pass

    if n == 1:
        total = t[i]
    else:
        total = t[i] + sum_subarray(t, i+1, n-1)

    cache[i, n] = total
    return total

length = 1000
t = [random.randint(-100, 100) for i in range(length)]

# find the total of all substrings, evaluated in order so
# that the recursive invocations are always in cache
for n in xrange(1, len(t)+1):
    for start in xrange(len(t)-n, -1, -1):
        total = sum_subarray(t, start, n)

# pull out the largest sum and the parameters that yield it
items = [(v, k) for k, v in cache.iteritems()]
print max(items)
