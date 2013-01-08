"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

class Vertex(object):
    """a Vertex is a node in a graph."""

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """return a string representation of this object that can
        be evaluated as a Python expression"""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """the str and repr forms of this object are the same"""


class SingleVertex(Vertex):
    """SingleVertex is a version of Vertex that makes sure that
    there is only one vertex with a given label"""

    # cache is a dictionary that maps from labels to Vertex object
    cache = {}

    def __new__(cls, label):
        """if a Vertex with (label) already exists, return
        a reference to it; otherwise create a new one (and store
        a reference in the cache).
        """
        try:
            return SingleVertex.cache[label]
        except KeyError:
            v = Vertex.__new__(cls, label)
            SingleVertex.cache[label] = v
            return v

    def __repr__(self):
        """return a string representation of this object that can
        be evaluated as a Python expression"""
        return 'SingleVertex(%s)' % repr(self.label)


class Edge(tuple):
    """an Edge is a list of two vertices"""

    def __new__(cls, *vs):
        """the Edge constructor takes two vertices as parameters"""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """return a string representation of this object that can
        be evaluated as a Python expression"""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """the str and repr forms of this object are the same"""


class Graph(dict):
    """a Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """create a new graph.  (vs) is a list of vertices;
        (es) is a list of edges."""
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """add (v) to the graph"""
        self[v] = {}


    def add_edge(self, e):
        """add (e) to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def remove_edge(self, e):
        """remove (e) from the graph"""
        v, w = e
        del self[v][w]
        del self[w][v]

    def get_edge(self, v, w):
        """return the edge (v, w) if it exists, None otherwise.

        has_edge is a synonym for get_edge"""
        try:
            return self[v][w]
        except KeyError:
            return None

    has_edge = get_edge

    def vertices(self):
        """return a list of vertices in this graph"""
        return self.keys()

    def edges(self):
        """return a list of the edges in this graph"""
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return list(s)

    def __repr__(self):
        return "Graph(%s, %s)" % (repr(self.vertices()), 
                                  repr(self.edges()))

    __str__ = __repr__

    def out_vertices(self, v):
        """ return a list of vertices that can be reached in one hop from v"""
        return self[v].keys()

    def out_edges(self, v):
        """return the list of edges out of v"""
        return self[v].values()

    def in_vertices(self, v):
        """return the list of vertices that can reach v in one hop"""
        return [d[v][0] for d in self.itervalues() if v in d]

    def in_edges(self, v):
        """return the list of edges into v"""
        return [d[v] for d in self.itervalues() if v in d]

    def add_all_edges(self):
        """make a complete graph by adding edges between all
        pairs of vertices"""
        vs = self.vertices()
        for i, v in enumerate(vs):
            for j, w in enumerate(vs):
                if j == i: break
                self.add_edge(Edge(v, w))
                

    def add_regular_edges(self, k=2):
        """make a regular graph with degree (k).  (k) must be even"""
        vs = self.vertices()
        if is_odd(k):
            if is_odd(len(vs)):
                raise ValueError, ("cannot build a regular graph with" +
                                   "an odd degree and an odd number of" +
                                   "vertices.")
            self.add_regular_edges_even(k-1)
            self.add_regular_edges_odd()
        else:
            self.add_regular_edges_even(k)

        
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_edge(Edge(v, w))


    def add_regular_edges_even(self, k=2):
        """make a regular graph with degree (k).  (k) must be even"""
        vs = self.vertices()
        double = vs * 2
        
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_edge(Edge(v, w))

    def add_regular_edges_odd(self):
        """add an extra edge "across" the graph to finish off a regular
        graph with odd degree"""
        vs = self.vertices()
        double = vs * 2
        
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_edge(Edge(v, w))

    def bfs(self, s, visit=None):
        "breadth first search"

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

    def isConnected(self):
        """return True if there is a path from any vertex to
        any other vertex in this graph; False otherwise
        """
        v = self.random_vertex()
        self.bfs(v)
        return False not in [v.visited for v in self]

    
def is_odd(x):
    """return a True value (1) if x is odd, a False value (0) otherwise"""
    return x % 2

def main(script, *args):

    vs = [SingleVertex(c) for c in 'abc']
    g = Graph(vs)
    g.add_regular_edges(2)

    print g

    g2 = eval(repr(g))
    print g2


if __name__ == '__main__':
    import sys
    main(*sys.argv)

