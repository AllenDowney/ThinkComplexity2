"""Wrapper class for the heapq module

For people who prefer object-oriented style, this wrapper class
provides a cleaner interface to the functions in the heapq module.  It
also provides some additional capabilities, including reduce, which is
useful in some graph algorithms.

A heap, as implemented by the heapq module, is a list that happens to
have the heap property, which is that there is no value of k such that
heap[k] > heap[2*k+1] or heap[k] > heap[2*k+2].  The heapq module
provides functions to transform a list into a heap and to add and
remove elements, among others.

Heap extends the list class, so Heaps provide all list methods, but
methods that modify the list might break the heap property.  The
is_heap method checks whether a Heap has the heap property.

The methods push, popmin, replace and heapify are just aliases for
heappush, heappop, heapreplace and heapify.  popmin is so named partly
to document its function and partly to avoid conflict with list.pop.

Specifying __slots__ is an optimization that saves memory, but it
makes it impossible to add additional attributes to a Heap.

pushpop is a variant of replace that optimizes the case where the item
being pushed would immediately be popped.

__iter__ returns a destructive iterator; each time next is invoked, it
pops an item from the heap.

reduce is sometimes called "reduce-key" in the context of graph
algorithms.  It replaces the item at the given position with a new
item (which must have lower value than the old item) and then restores
the heap property.

The test code demonstrates the use of each method.


Copyright 2005 Allen B. Downey

This program combines ideas of mine with suggestions posted on
Python-dev by Raymond Hettinger, Jeremy Fincher and Scott David
Daniels.  It also contains code from the Python implementation of the
heapq module, which was written by Kevin O'Connor and augmented by Tim
Peters and Raymond Hettinger.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see http://www.gnu.org/licenses/gpl.html
    or write to the Free Software Foundation, Inc., 51 Franklin St, 
    Fifth Floor, Boston, MA  02110-1301  USA

"""

import heapq

class Heap(list):
    """This is a wrapper class for the heap functions provided
    by the heapq module.
    """
    __slots__ = ()
    
    def __init__(self, t=[]):
        self.extend(t)
        self.heapify()

    def heapify(self): heapq.heapify(self)
    def push(self, item): heapq.heappush(self, item)
    def popmin(self): return heapq.heappop(self)
    def replace(self, item): return heapq.heapreplace(self, item)

    def peek(self): return self[0]

    def pushpop(self, item):
        "Pushes the item onto the heap and then pop the smallest value"
        if self and self[0] < item:
            return heapq.heapreplace(self, item)
        return item
 
    def __iter__(self):
        "Returns a destructive iterator over the heap's elements"
        try:
            while True:
                yield self.popmin()
        except IndexError:
            pass

    def reduce(self, pos, newitem):
        "Replaces self[pos] with a lower value item and reheapifies."
        while pos > 0:
            parentpos = (pos - 1) >> 1
            parent = self[parentpos]
            if parent <= newitem:
                break
            self[pos] = parent
            pos = parentpos
        self[pos] = newitem

    def is_heap(self):
        "Returns True if the heap has the heap property; False otherwise"
        n = len(self)
        # The largest index there's any point to looking at
        # is the largest with a child index in-range, so must have 2*i + 1 < n,
        # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
        # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
        # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
        try:
            for i in xrange(n//2):
                if self[i] > self[2*i+1]: return False
                if self[i] > self[2*i+2]: return False
        except IndexError:
            pass
        return True
        

def heapsort(seq):
    """Makes a new sorted list from a sequence.

    Uses a Heap.
    """
    return [x for x in Heap(seq)]


if __name__ == '__main__':
    from random import randint, shuffle

    # generate a random test case
    n = 15
    data = [randint(1,n) for i in xrange(n)]
    shuffle(data)
    print data

    # test the constructor
    heap = Heap(data)
    print heap, heap.is_heap()

    # test popmin
    sorted = []
    while heap:
        sorted.append(heap.popmin())
    
    data.sort()
    print heap, heap.is_heap()
    print data == sorted

    # test 2
    shuffle(data)
    print data

    # test push
    for item in data:
        heap.push(item)
    print heap, heap.is_heap()

    # test __iter__
    sorted = [x for x in heap]

    data.sort()
    print data == sorted

    # test 3
    shuffle(data)
    print data
    heap = Heap(data)
    print heap, heap.is_heap()

    # test reduce
    for i in range(5):
        pos = randint(0,n-1)
        decr = randint(1,10)
        item = heap[pos] - decr
        heap.reduce(pos, item)

    # test is_heap
    heap = Heap(data)
    count = 0
    while 1:
        shuffle(heap)
        if heap.is_heap():
            print heap
            break
        else:
            count += 1
    print 'It took', count, 'tries to find a heap by chance.'

    print heapsort(data)
    
    try:
        heap.x = 5
    except AttributeError:
        print "Can't add attributes."
