import string
from math import sqrt
from random import *

class Vertex(str):
    "a vertex is a simple object"
    def __init__(self, *args):
        str.__init__(self, *args)
        self.randomPos()
        
    def randomPos(self):
        self.x = uniform(-10, 10)
        self.y = uniform(-10, 10)

    def pos(self):
        return self.x, self.y

    def distanceFrom(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)

class Edge(tuple):
    "an edge is a 2-tuple of vertices"
    def __init__(self, *args):
        tuple.__init__(self, *args)
        self.length = self[0].distanceFrom(self[1])

    def reverse(self):
        "return a new edge with swapped vertices"
        return Edge((self[1], self[0]))
    
class Graph(dict):
    "a graph is a map from vertices to lists of edges"
    def __init__(self, vs, es, directed=False):
        if directed==False:
            res = [e.reverse() for e in es]
            es = uniqueEdges(es + res)

        for v in vs:
            self[v] = {}

        for e in es:
            self[e[0]][e[1]] = e

    def vertices(self):
        """return an iterator that enumerates the vertices in this graph"""
        return self.iterkeys()

    def edges(self):
        """return a list of the edges in this graph"""
        es = []
        for d in self.itervalues():
            es.extend(d.itervalues())
        return es

    def findEdge(self, v, w):
        """return the edge v->w or raise KeyError if it doesn't exist"""
        return self[v][w]

    def hasEdge(self, v, w):
        """return the edge (v, w) if it exists, false otherwise"""
        try:
            return self[v][w]
        except KeyError:
            return False

    def outVertices(self, v):
        """ return a list of vertices that can be reached in one hop from v"""
        return self[v].iterkeys()

    def outEdges(self, v):
        """return the list of edges out of v"""
        return self[v].itervalues()

    def inVertices(self, v):
        """return the list of vertices that can reach v in one hop"""
        return [d[v][0] for d in self.itervalues() if v in d]

    def inEdges(self, v):
        """return the list of edges into v"""
        return [d[v] for d in self.itervalues() if v in d]

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
            queue.extend(self.outVertices(v))

    def isConnected(self):
        self.bfs(self.vertices().next())
        return False not in [v.visited for v in self]

        
def uniqueEdges(es):
    t = [(e, True) for e in es]
    d = dict(t)
    return d.keys()

def makeRandomEdge(vs):
    while True:
        v1 = choice(vs)
        v2 = choice(vs)
        if v1 != v2: break
    return Edge((v1, v2))

def makeRandomGraph(vs, p=0.05):
    es = []
    for v in vs:
        for w in vs:
            if v == w: continue
            if random() > p: continue
            es.append(Edge((v, w)))
    return Graph(vs, es)

vs = [Vertex(c) for c in string.lowercase + string.uppercase]
g = makeRandomGraph(vs)

print g.isConnected()

