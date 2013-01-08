""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import math
import random
import string
import sys

from Heap import Heap
from Graph import Edge, Vertex
from GraphWorld import GraphWorld
from RandomGraph import RandomGraph


def avg(seq):
    return 1.0 * sum(seq) / len(seq)

Inf = float('Inf')

class SmallWorldGraph(RandomGraph):

    def __init__(self, vs, k, p):
        RandomGraph.__init__(self, vs)
        self.add_regular_edges(k=k)
        self.rewire(p=p)
        self.assign_edge_lengths()

    def assign_edge_lengths(self):
        """Gives each edge a length attribute."""
        for e in self.edges():
            e.length = 1

    def shortest_path_tree(self, s, hint=None):
        """Finds the length of the shortest path from Vertex (s) to the
        other Vertices; stores the path lengths as a dist attribute.
        (uses Dijkstra's algorithm).

        In theory this is a bad implementation of Dijkstra's algorithm:
        it keeps the priority queue as a sorted list and re-sorts after
        processing each vertex.

        But in practice this turns out to be pretty good, because Python's
        sort algorithm is fast for lists that are almost sorted.

        hint: a dictionary that maps from tuples (v,w) to already-known
        shortest path length from v to w.
        """
        if hint == None:
            hint = {}

        # initialize distance attribute for each vertex
        for v in self.iterkeys():
            v.dist = hint.get((s, v), Inf)
        s.dist = 0

        # start with all vertices in the queue
        queue = [v for v in self if v.dist < Inf]
        flag = True
        
        while len(queue) > 0:

            # re-sort the queue if necessary, then pop the lowest item
            if flag:
                queue.sort(key=lambda v: v.dist)
            flag = False
            v = queue.pop(0)
            
            # for each neighbor of v, see if we found a new shortest path
            for w, e in self[v].iteritems():
                new = v.dist + e.length
                if w.dist > new:
                    w.dist = new
                    queue.append(w)
                    flag = True
                    
    def shortest_path_tree2(self, s, hint=None):
        """A Heap-based implementation of Dijkstra's algorithm
        based on Connelly Barnes's modification of David Eppstein's
        code at
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466
        """
        for v in self:
            v.dist = Inf

        queue = Heap([(0, s)])
        
        while len(queue) > 0:

            (cost, v) = queue.popmin()
            if v.dist < Inf: 
                continue
            v.dist = cost
            
            for w, e in self[v].iteritems():
                if w.dist < Inf:
                    continue
                new = v.dist + e.length
                queue.push((new, w))

    def init_all_pairs(self):
        """For the all pairs shortest path algorithms, compute the
        weight dictionary W, where W[i,j] is the length of the edge from
        i to j if there is one, infinity if there isn't and 0 if i==j
        """
        W = {}
        for i, d in enumerate(self.itervalues()):
            for j, w in enumerate(self.iterkeys()):
                try:
                    W[i,j] = d[w].length
                except:
                    W[i,j] = Inf
            W[i,i] = 0
        return W

    def extend_shortest_paths(self, D, W):
        """Multiply the path dictionary D by the weight dictionary W.
        This is part of the 'repeated squaring' algorithm.
        See Cormen Leiserson and Rivest, page 554.
        """
        indices = range(len(self))
        E = {}
        for i in indices:
            for j in indices:
                t = [D[i,k] + W[k,j] for k in indices]
                E[i,j] = min(t)
        return E

    def all_pairs_shortest_path(self):
        """Finds the shortest path between all pairs of vertices using
        the the 'repeated squaring' algorithm.
        See Cormen Leiserson and Rivest, page 556.

        In theory this algorithm is not as fast as Floyd-Warshall,
        but because the innermost loop can be written as a list
        comprehension, it does pretty well.
        """
        n = len(self)
        W = self.init_all_pairs()        
        D = W
        i = 1
        while i<n:
            D = self.extend_shortest_paths(D, D)
            i *= 2

        return D


    def all_pairs_floyd_warshall(self):
        """Finds the shortest path between all pairs of nodes using
        the Floyd-Warshall algorithm.
        See Cormen Leiserson and Rivest, page 560.
        """
        n = len(self)
        indices = range(n)
        W = self.init_all_pairs()

        # d is a dictionary that maps from an index, k, to the
        # weight matrix W_k
        d = {-1: W}
        for k in indices:
            d[k] = {}
            for i in indices:
                for j in indices:
                    d[k][i,j] = min(d[k-1][i,j], d[k-1][i,k] + d[k-1][k,j])

        D = d[n-1]
        return D


    def recursive_floyd_warshall(self):
        """Finds the shortest path between all pairs of nodes using
        the Floyd-Warshall algorithm.
        """
        cache = {}
        def shortest_path(i, j, k):
            """Finds the shortest path from i to j using only
            vertices 0 through k as intermediaries.
            """
            if (i,j,k) in cache:
                return cache[i,j,k]

            length = min(shortest_path(i, j, k-1),
                         shortest_path(i, k, k-1) + shortest_path(k, j, k-1))

            cache[i,j,k] = length
            return length

        n = len(self)
        indices = range(n)
        W = self.init_all_pairs()

        # preload the cache
        for key, val in W.iteritems():
            i, j = key
            cache[i,j,-1] = val

        # compute all-pairs shortest paths
        d = {}
        for i in indices:
            for j in indices:
                d[i,j] = shortest_path(i, j, n-1)

        return d


    def diameter(self):
        """Finds the diameter of the graph."""

        # choose an arbitrary start vertex and
        # compute the shortest path tree
        v = self.iterkeys().next()
        self.shortest_path_tree(v)

        # find the farthest vertex and use it as the
        # start vertex for another shortest path tree
        d, v = max([(v.dist, v) for v in self])
        self.shortest_path_tree(v)

        # find the farthest vertex again and return its distance
        d, v = max([(v.dist, v) for v in self])
        return d


    def char_length(self):
        """Computes the characteristic length of the graph according
        to the definition in Watts and Strogatz.

        Uses Dijkstra's algorithm from all vertices.

        Precondition: the graph is connected.
        """
        # for each vertex v, d[v] is the list of other vertices
        # and their distances
        d = {}
        for v in self:
            self.shortest_path_tree(v, d)
            t = [((w,v), w.dist) for w in self if w is not v]
            d.update(t)

        # return the average of all values
        return avg(d.values())

    def char_length2(self):
        """Computes the characteristic length of the graph according
        to the definition in Watts and Strogatz.  Uses the repeated
        squaring algorithm to compute all pairs shortest paths.

        Precondition: the graph is connected.
        """
        n = len(self)
        D = self.all_pairs_shortest_path()
        t = [D[i,j] for i in range(n) for j in range(n) if i!=j]
        return avg(t)

    def char_length3(self):
        """Computes the characteristic length of the graph according
        to the definition in Watts and Strogatz.  Uses the Floyd-Warshall
        algorithm to compute all pairs shortest paths.

        Precondition: the graph is connected.
        """
        n = len(self)
        D = self.all_pairs_floyd_warshall()
        t = [D[i,j] for i in range(n) for j in range(n) if i!=j]
        return avg(t)

    def char_length4(self):
        """Computes the characteristic length of the graph according
        to the definition in Watts and Strogatz.  Uses the Floyd-Warshall
        algorithm to compute all pairs shortest paths.

        Precondition: the graph is connected.
        """
        n = len(self)
        D = self.recursive_floyd_warshall()
        t = [D[i,j] for i in range(n) for j in range(n) if i!=j]
        return avg(t)

    def cluster_coef(self):
        """Computes the cluster coefficient of the graph according
        to the definition in Watts and Strogatz.
        """
        C = {}

        # for each vertex, C[v] is C_v, the cluster coefficient
        for v in self:
            set = self.out_vertices(v)
            C[v] = self.cluster(set)

        # the cluster coefficient for the graph is the average of C_v
        cvs = C.values()
        return avg(cvs)

    def cluster(self, set):
        """Returns the fraction of edges among this set that exist"""
        k = len(set)
        if k < 2: return 1.0
        possible = k * (k-1.0)
        edges = [1 for v in set for w in set if self[v].get(w, False)]
        return len(edges) / possible

    def rewire(self, p=0.01):
        """Rewires edges according to the algorithm in Watts and Strogatz.
        (p) is the probability that each edge is rewired.
        """
        # consider the edges in random order (this is slightly different
        # from Watts and Strogatz
        es = list(self.edges())
        random.shuffle(es)
        vs = self.vertices()
        
        for e in es:
            # if this edge is chosen, remove it...
            if random.random() > p: continue
            v, w = e
            self.remove_edge(e)

            # then generate a new edge that connects v to another vertex
            while True:
                w = random.choice(vs)
                if v is not w and not self.has_edge(v, w): break

            self.add_edge(Edge(v, w))

def name_generator():
    """this function generates Vertex names in the form a1, b1, ... z1,
    a2, b2, ... z2, etc.
    """
    i = 1
    while True:
        for c in string.lowercase:
            yield c + str(i)
        i += 1

def main(script, n='52', k='5', p='0.1', *args):
    random.seed(17)

    # create n Vertices
    n = int(n)
    k = int(k)
    p = float(p)

    names = name_generator()
    vs = [Vertex(names.next()) for c in range(n)]

    # create a graph
    g = SmallWorldGraph(vs, k, p)

    from time import clock

    print 'number of edges = ', len(g.edges())
    print 'Is connected?', g.is_connected()
    print 'diameter = ', g.diameter()

    start = clock()
    print 'char_length = ', g.char_length()
    print clock()-start
    
    start = clock()
    print 'char_length2 = ', g.char_length2()
    print clock()-start

    start = clock()
    print 'char_length3 = ', g.char_length3()
    print clock()-start

    start = clock()
    print 'char_length4 = ', g.char_length4()
    print clock()-start

    print 'cluster_coef = ', g.cluster_coef()
   
    # draw the graph
    draw = False
    if draw:
        layout = CircleLayout(g)
        gw = GraphWorld()
        gw.show_graph(g, layout)
        gw.mainloop()


if __name__ == '__main__':
    import sys
    main(*sys.argv)


