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
        

class Graph(dict):
    # old methods omitted...

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

        
