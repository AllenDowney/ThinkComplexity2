import sys
import urllib
import xml.dom.minidom
import string, random, operator
from math import sqrt
from Gui import *

class GraphCanvas(GuiCanvas):
    def drawVertex(self, v, r=0.4):
        tag = 'v%d' % id(self)
        self.create_circle(v.x, v.y, r, 'yellow', tags=tag)
        self.create_text(v.pos(), v, 'black', tags=tag)
        return tag

    def drawEdge(self, e):
        v, w = e
        tag = self.create_line([v.pos(), w.pos()])
        return tag

class GraphWorld(Gui):
    def __init__(self):
        Gui.__init__(self)
        self.setup()

    def setup(self):
        self.ca_width = 400
        self.ca_height = 400
        xscale = self.ca_width / 20
        yscale = self.ca_height / 20

        # left frame
        self.row()
        transforms = [ CanvasTransform(self.ca_width, self.ca_height,
                                       xscale, yscale) ]
        self.canvas = self.widget(GraphCanvas,
                              width=self.ca_width, height=self.ca_height,
                              bg='white', transforms=transforms)
        self.endfr()

        # right frame
        self.col()

        self.row([1,1])
        self.bu(text='Clear', command=self.clearGraph)
        self.bu(text='Quit', command=self.quit)
        self.endrow()
        
        self.endcol()

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
        print self.etags, self.vtags


class Vertex:
    def __init__(self, name):
        self.name = name
        self.randomPos()
        
    def randomPos(self):
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)

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

    vertices = dict.keys
    edges = dict.values

    def findEdge(self, v, w):
        return self[v][w]

    def hasEdge(self, v, w):
        return w in self[v]

    def outVertices(self, v): return self[v].iterkeys()

    def outEdges(self, v): return self[v].itervalues()

    def inVertices(self, v):
        return [w for d in self.itervalues() for w in d if w == v]

    def inEdges(self, v):
        return [e for d in self.itervalues()
                for e in d.itervalues() if e[1] == v]

    def bfs(self, s, visit=None):
        "breadth first search"

        # mark all the vertices unvisited
        for v in self: v.visited = False

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
        self.bfs(self.iterkeys().next())
        return False not in [v.visited for v in self]


    def shortestPathTree(self, s):
        """form the shortest path tree from start node s by
        labelling each vertex with its distance from s and
        its predecessor in the path from s
        """
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
        """find and return the diameter of the graph
        """

        # choose an arbitrary start vertex and
        # compute the shortest path tree
        v = self.iterkeys().next()
        vs = self.shortestPathTree(v)

        # find the farthest vertex and use it as the
        # start vertex for another shortest path tree
        d, v = max([(v.dist, v) for v in vs])
        self.shortestPathTree(v)

        # find the farthest vertex again and return its distance
        d, v = max([(v.dist, v) for v in vs])
        return d

    def charLength(self):
        """compute the characteristic length of the graph according
        to the definition in Watts and Strogatz.

        Precondition: the graph is connected.
        """
        d = {}

        # for each vertex v, d[v] is the list of other vertices
        # and their distances
        for v in self:
            self.shortestPathTree(v)
            d[v] = [w.dist for w in self if w is not v]

        # join all the lists and return the average of all values
        ds = sum(d.itervalues(), [])
        return sum(ds) / len(ds)

    def clusterCoef(self):
        """compute the cluster coefficient of the graph according
        to the definition in Watts and Strogatz.
        """
        d = {}

        # for each vertex, d[v] is C_v, the cluster coefficient
        for v in self:
            set = self.outVertices(v) + [v]
            d[v] = self.cluster(set)

        # the cluster coefficient for the graph is the average of C_v
        ds = d.itervalues()
        return sum(ds) / len(d)

    def cluster(self, set):
        "return the fraction of edges among this set that exist"
        k = len(set)
        possible = k * (k-1.0)
        edges = [1 for v in set for w in set if self.hasEdge(v, w)]
        return len(v) / possible

        
class Queue(list):
    """this class is a subclass of list that maintains
    a parallel dictionary so that it can check membership
    in constant time.  It maintains the equivalence of the
    list and the dictionary by overriding pop and append;
    using any other modifiers will break the invariant.
    """
    def __init__(self, seq):
        list.__init__(self, seq)
        self.set = dict(zip(seq, seq))

    def pop(self, i=-1):
        return self.set.pop(list.pop(self, i))

    def append(self, x):
        list.append(self, x)
        self.set[x] = x

    def __contains__(self, x):
        return x in self.set
        
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

def spreadVertex(v, others, minDist=1.0):
    while True:
        t = [(v.distanceFrom(w), w) for w in others]
        d, w = min(t)
        if d > minDist:
            print d
            break
        print 'try again'
        minDist *= 0.9
        v.randomPos()
        
def spreadVertices(vs):
    others = vs[:]
    for v in vs:
        others.remove(v)
        spreadVertex(v, others)
        others.append(v)

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

def sortByDistance(v, others):
    t = [(v.distanceFrom(w), w) for w in others]
    t.sort()
    return [w for (d, w) in t]

def localGraph(vs, k=3):
    es = []
    others = vs[:]
    for v in vs:
        others.remove(v)
        t = sortByDistance(v, others)
        for w in t[:k]:
            es.append(Edge((v,w)))
        others.append(v)
    return Graph(vs, es)

def findcity(city, state):
    def getText(nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
            elif node.hasChildNodes():
                rc = rc + getText(node.childNodes)
        return rc
    
    url = (("http://terraserver.microsoft.net/TerraService.asmx/GetPlaceList?" +
            "placeName=%s&MaxItems=1&imagePresence=false")
           % (string.replace(city, " ", "+") + "%2C+" + state))
    inf = urllib.FancyURLopener().open(url)
    dom = xml.dom.minidom.parse(inf)
    inf.close()
    placeFacts = dom.getElementsByTagName("PlaceFacts")
    center = placeFacts[0].getElementsByTagName("Center")
    lat = string.atof(getText(center[0].getElementsByTagName("Lat")))
    lon = string.atof(getText(center[0].getElementsByTagName("Lon")))
    return lon, lat


print findcity('needham', 'ma')
sys.exit()

vs = [Vertex(c) for c in string.lowercase + string.uppercase]
spreadVertices(vs)

es = [randomEdge(vs, v) for v in vs]
es += [randomEdge(vs) for i in range(1000)]
es = uniqueEdges(es)

#for v in vs:
#    print v, v.x, v.y

#for e in es:
#    print e, e.length

#g = Graph(vs, es)

#import Lumpy
#lumpy = Lumpy.Lumpy()
#lumpy.make_reference()
g = localGraph(vs)
#lumpy.object_diagram()
 

#print g.isConnected()

#print g.diameter()

#print g.charLength()
#print g.clusterCoef()


#gw = GraphWorld()
#gw.showGraph(g)
#gw.mainloop()
