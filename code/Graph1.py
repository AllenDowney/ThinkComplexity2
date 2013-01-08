import string, random, operator
from math import sqrt

class Vertex(object):
    def __init__(self, name):
        """initialize a new vertex.
           a vertex has a name and a position
        """
        self.name = name
        self.randomPos()
        
    def randomPos(self):
        """choose a random position for this vertex"""
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)

    def pos(self):
        """return a 2-tuple with the position of this vertex"""
        return self.x, self.y

    def distanceFrom(self, other):
        """return the distance from this vertex to another"""
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)

class Edge(tuple):
    "an edge is a 2-tuple of vertices"

    def __init__(self, *args):
        # invoke the constructor from the parent class
        tuple.__init__(self, *args)
        self.length = self[0].distanceFrom(self[1])

    def reverse(self):
        "return a new edge with swapped vertices"
        return Edge((self[1], self[0]))
    
class Graph(dict):
    """a graph is a dictionary of dictionaries.  The first
    dictionary maps from a vertex to an inner dictionary.
    The second dictionary maps from other vertices to the
    edges that connect them.  Another way to say the same
    thing is that for vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs, es, directed=False):
        """create a new graph.  vs is a list of vertices;
        es is a list of edges."""

        # if the graph is undirected, then make sure that for
        # every edge a->b, we also have b->a
        if directed==False:
            res = [e.reverse() for e in es]
            es = uniqueEdges(es + res)

        # create a dictionary for each vertex
        for v in vs:
            self[v] = {}

        # add the edges to the graph
        for e in es:
            self[e[0]][e[1]] = e

    def edges(self):
        """return a list of the edges in this graph"""
        return None

    def findEdge(self, v, w):
        """return the edge v->w or raise KeyError if it doesn't exist"""
        return None

    def hasEdge(self, v, w):
        """return true if v->w exists, false otherwise"""
        return None

    def outVertices(self, v):
        """ return a list of vertices that can be reached in
        one hop from v"""
        return None

    def outEdges(self, v):
        """return the list of edges out of v"""
        return None

    def inVertices(self, v):
        """return the list of vertices that can reach v in one hop"""
        return None

    def inEdges(self, v):
        """return the list of edges into v"""
        return None

    def isConnected(self):
        """return true if the graph is connected, false otherwise"""
        return None

def uniqueEdges(es):
    t = [(e, True) for e in es]
    d = dict(t)
    return d.keys()

def randomEdge(vs, v1=None, v2=None):
    v1 = v1 or randomVertex(vs)
    v2 = v2 or randomVertex(vs)
    while v1 == v2:
        v1 = randomVertex(vs)
        v2 = randomVertex(vs)
    return Edge((v1, v2))

def randomVertex(vs):
    return random.choice(vs)

def randomGraph(vs, k=3):
    es = []
    others = vs[:]
    for v in vs:
        others.remove(v)
        random.shuffle(others)
        for w in others[:k]:
            es.append(Edge((v,w)))
        others.append(v)
    return Graph(vs, es)

vs = [Vertex(c) for c in string.lowercase + string.uppercase]
es = [randomEdge(vs) for i in range(200)]
es = uniqueEdges(es)

g = Graph(vs, es)
