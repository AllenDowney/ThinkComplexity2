""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

class Vertex(object):
    """A Vertex is a node in a graph."""

    # cache is a dictionary that maps from labels to Vertex object
    cache = {}

    def __new__(cls, label):
        """if a Vertex with (label) already exists, return
        a reference to it; otherwise create a new one (and store
        a reference in the cache).
        """
        try:
            return Vertex.cache[label]
        except KeyError:
            v = object.__new__(cls)
            Vertex.cache[label] = v
            return v

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """Returns a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Edge(tuple):
    """An Edge is a list of two vertices."""

    def __new__(cls, e1, e2):
        """The Edge constructor takes two vertices."""
        return tuple.__new__(cls, (e1, e2))

    def __repr__(self):
        """Return a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Graph(dict):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """Creates a new graph.  
        vs: list of vertices;
        es: list of edges.
        """
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        self[v] = {}

    def add_edge(self, e):
        """Adds an edge to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def remove_edge(self, e):
        """Removes (e) from the graph."""
        v, w = e
        del self[v][w]
        del self[w][v]

    def get_edge(self, v, w):
        """Returns the edge (v, w) if it exists, None otherwise.

        has_edge is a synonym for get_edge"""
        try:
            return self[v][w]
        except KeyError:
            return None

    has_edge = get_edge

    def vertices(self):
        """Returns a list of vertices in this graph."""
        return self.keys()

    def edges(self):
        """Returns a set of the edges in this graph."""
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return s

    def out_vertices(self, v):
        """Returns a list of vertices that can be reached in one hop from v."""
        return self[v].keys()

    def out_edges(self, v):
        """Returns the list of edges out of v."""
        return self[v].values()

    def add_all_edges(self):
        """Makes a complete graph by adding edges between all
        pairs of vertices."""
        vs = self.vertices()
        for i, v in enumerate(vs):
            for j, w in enumerate(vs):
                if j == i: break
                self.add_edge(Edge(v, w))
                
    def add_regular_edges(self, k=2):
        """Make a regular graph with degree k if possible;
        otherwise raises an exception."""
        vs = self.vertices()
        if k >= len(vs):
            raise ValueError, ("cannot build a regular graph with " +
                               "degree >= number of vertices.")

        if is_odd(k):
            if is_odd(len(vs)):
                raise ValueError, ("cannot build a regular graph with " +
                                   "an odd degree and an odd number of " +
                                   "vertices.")
            self.add_regular_edges_even(k-1)
            self.add_regular_edges_odd()
        else:
            self.add_regular_edges_even(k)

    def add_regular_edges_even(self, k=2):
        """Make a regular graph with degree k.  k must be even"""
        vs = self.vertices()
        double = vs * 2
        
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_edge(Edge(v, w))

    def add_regular_edges_odd(self):
        """Adds an extra edge "across" the graph to finish off a regular
        graph with odd degree.  The number of vertices must be even."""
        vs = self.vertices()
        n = len(vs)
        reduplicated_list = vs * 2
        
        for i in range(n/2):
            v = reduplicated_list[i]
            w = reduplicated_list[i+n/2]
            self.add_edge(Edge(v, w))

    def bfs(self, s, visit=None):
        """Breadth first search.

        s: start vertex
        visit: function called on each vertex
        """

        # mark all the vertices unvisited
        for v in self.vertices():
            v.visited = False

        # initialize the queue with the start vertex
        queue = [s]
        
        while queue:

            # get the next vertex
            v = queue.pop(0)

            # skip it if it's already marked
            if v.visited: continue

            # mark it visited, then invoke visit
            v.visited = True
            if visit: visit(v)

            # add its out vertices to the queue
            queue.extend(self.out_vertices(v))


def is_odd(x):
    """Returns a True value (1) if x is odd, a False value (0) otherwise"""
    return x % 2


def main(script, *args):
    v = Vertex('v')
    print v
    w = Vertex('w')
    print w
    e = Edge(v, w)
    print e
    g = Graph([v,w], [e])
    print g

    vs = [Vertex(c) for c in 'abc']
    g = Graph(vs)
    g.add_regular_edges(2)

    print g

    g2 = eval(repr(g))
    print g2


if __name__ == '__main__':
    import sys
    main(*sys.argv)


