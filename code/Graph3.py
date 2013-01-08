import string
from math import sqrt
from random import *
from Gui import *

class GraphCanvas(GuiCanvas):
    def drawVertex(self, v, r=0.4):
        tag = 'v%d' % id(self)
        self.circle([v.x, v.y], r, 'yellow', tags=tag)
        self.text(v.pos(), v, 'black', tags=tag)
        return tag

    def drawEdge(self, e):
        v, w = e
        tag = self.line([v.pos(), w.pos()])
        return tag

class GraphWorld(Gui):
    def __init__(self):
        Gui.__init__(self)
        self.setup()

    def setup(self):
        self.ca_width = 400
        self.ca_height = 400
        xscale = self.ca_width / 21
        yscale = self.ca_height / 21

        self.canvas = self.widget(GraphCanvas,
                              width=self.ca_width, height=self.ca_height,
                              bg='white', transforms=[])
        transform = CanvasTransform(self.canvas, [xscale, yscale])
        self.canvas.add_transform(transform)

    def clearGraph(self):
        tags = self.vtags + sum(self.etags.itervalues(), [])
        for tag in tags:
            self.canvas.delete(tag)

    def showGraph(self, g):
        c = self.canvas
        self.etags = {}
        for v in g:
            self.etags[v] = [c.drawEdge(e) for e in g.outEdges(v)]

        self.vtags = [c.drawVertex(v) for v in g]


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

    def shortestPathTree(self, s):
        for v in self:
            v.dist = None
            v.p = None
        s.dist = 0
        queue = Queue([s])
        while queue:
            v = queue.pop(0)
            for w, e in self[v].iteritems():
                if w.dist is not None and w.dist < v.dist + e.length:
                    continue
                w.dist = v.dist + e.length
                w.p = v
                if w not in queue: queue.append(w)
        return [v for v in self if v.dist is not None]

    def diameter(self):
        v = self.iterkeys().next()
        vs = self.shortestPathTree(v)

        d, v = max([(v.dist, v) for v in vs])
        
        self.shortestPathTree(v)
        d, v = max([(v.dist, v) for v in vs])

        while v:
            if v.p:
                e = self.findEdge(v.p, v)
            v = v.p
        
        return d

    def charLength(self):
        d = {}
        for v in self:
            self.shortestPathTree(v)
            d[v] = [w.dist for w in self if w is not v]
        ds = sum(d.itervalues(), [])
        return sum(ds) / len(ds)

    def clusterCoef(self):
        d = {}
        for v in self:
            set = self.outVertices(v) + [v]
            d[v] = self.cluster(set)
        ds = d.itervalues()
        return sum(ds) / len(d)

    def cluster(self, set):
        "return the fraction of edges among this set that exist"
        k = len(set)
        possible = k * (k-1.0)
        edges = [1 for v in set for w in set if self.hasEdge(v, w)]
        return len(v) / possible

    def diameter(self):
        v = self.iterkeys().next()
        vs = self.shortestPathTree(v)

        d, v = max([(v.dist, v) for v in vs])
        
        self.shortestPathTree(v)
        d, v = max([(v.dist, v) for v in vs])

        while v:

            if v.p:
                e = self.findEdge(v.p, v)

            v = v.p
        
        return d

        
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
    for i, v in enumerate(vs):
        for w in vs[i+1:]:
            if random() > p: continue
            es.append(Edge((v, w)))
            es.append(Edge((w, v)))
    return Graph(vs, es, directed=True)

def sortByDistance(v, vs):
    t = [(v.distanceFrom(w), w) for w in vs if w!=v]
    t.sort()
    return [w for (d, w) in t]

def kClosest(v, vs, k=3):
    """of the other vertices in vs, return the k closest to v"""
    t = [(v.distanceFrom(w), w) for w in vs if w!=v]
    map = dict(t)
    return [map.pop(min(map)) for i in range(k)]
    
def makeLocalGraph(vs, k=3):
    es = [Edge((v,w)) for v in vs for w in kClosest(v, vs, k)]
    return Graph(vs, es)

def spreadVertex(v, others, minDist=1.0):
    while True:
        t = [(v.distanceFrom(w), w) for w in others]
        d, w = min(t)
        if d > minDist:
            break
        minDist *= 0.9
        v.randomPos()
        
def spreadVertices(vs):
    others = vs[:]
    for v in vs:
        others.remove(v)
        spreadVertex(v, others)
        others.append(v)


vs = [Vertex(c) for c in string.lowercase + string.uppercase]
spreadVertices(vs)

g = makeLocalGraph(vs)
print g.isConnected()

gw = GraphWorld()
gw.showGraph(g)
gw.mainloop()
