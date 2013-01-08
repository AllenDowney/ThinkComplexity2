from Graph import Graph, Vertex
import random
from GraphWorld import GraphWorld,GraphCanvas,Layout,CircleLayout,RandomLayout
import DirectedGraphWorld

class Arc(tuple):
    """
    Represents a Directed arc FROM Directed Vertex v TO Directed Vertex w.
    """
    def __new__(cls, *vs):
        """The Arc Constructor takes two vertices"""
        if len(vs) != 2:
            raise ValueError, 'Arcs must connect exactly two vertices'
        return tuple.__new__(cls,vs)
    
    def __repr__(self):
        """Return a string representation of this arc
         that can be evaluated as a Python expression."""
        return 'Arc(%s to %s)' %(repr(self[0]), repr(self[1]))
    
    __str__ = __repr__

    
class DirectedGraph(Graph):
    """A DirectedGraph contains two dictionaries.
    The internal dictionary is a dictionary of dictionaries.
    It maps vertices to their out-arcs. The reverse dictionary
    maps vertices to their in-arcs.
    """

    def __init__(self,vs=[],es=[]):
        """
        Creates a new directed graph. 
        @Args:
            vs, a list of Vertices 
            es, a list of Arcs
        @Returns:
            None
        """
        self.reverse_graph = {} #keeps a map of in-vertices
        for v in vs:
            self.add_vertex(v)
        for e in es:
            self.add_arc(e)
 
    def add_vertex(self, v):
        """
        Adds a vertex to both the DirectedGraph and its internal complement
        dictionary, and initiates its value as an empty dictionary.
        @Args:
            A Vertex v
        @Returns:
            None
        """
        self[v] = {}
        self.reverse_graph[v] = {}
    
    def add_arc(self, e):
        """
        Creates an arc FROM v TO w (As a value of v in the internal dictionary).
        Adds same arc TO w FROM v (As a value of w in the reverse dictionary).
        @Args:
            An Arc e
        @Returns: 
            None
        """
        v, w = e
        if v == w:
            raise LoopError('An arc cannot exist from a vertex to itself.')
        self[v][w] = e
        self.reverse_graph[w][v] = e
    
    add_edge = add_arc
    """We only want to add arcs, not edges"""
        
    def remove_arc(self, v, w):
        """Deletes the directed arc FROM v TO w."""
        del self[v][w]
        del self.reverse_graph[w][v]
    
    remove_edge = remove_arc
    """arcs, not edges."""
    
    def get_out_arc(self, v, w):
        """
        Tries to return the directed arc FROM v TO w. If no arc exists,
        returns None.
        """
        try:
            return self[v][w]
        except KeyError:
            return None

    has_out_arc = get_out_arc   
    
    def get_in_arc(self, v, w):
        """
        Tries to return the directed arc TO w FROM w. Returns None if no such
        arc exists. Vim is cool.
        """
        try:
            return self.reverse_graph[v][w]
        except KeyError:
            return None
    
    has_in_arc = get_out_arc
    
    def has_arc(self,v,w):
        """If an arc between v and w (in either direction) exists in the graph 
        or the reverse_graph, returns True.otherwise returns False."""
        if self.get_in_arc(v,w) or self.get_out_arc(v,w):
            return True
        else:
            return False

    def get_edge(self, v, w):
        raise NotApplicableToDirectedGraphsError('Please use get_out_arc or get_in_arc to get a handle on arcs in a DirectedGraph')
    
    def arcs(self):
        """returns a set of all out-arcs of the graph"""
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return s
    
    edges = arcs
    
    def in_arcs(self, v):
        """returns a set of all in-arcs of the graph"""
        s = set()
        for w in self.reverse_graph[v]:
            s.update(self.reverse_graph[v][w])
        return s

    def in_degree(self,v):
        """takes a vertex and returns the number
    of arcs going into it (the in-degree)"""
        try:
            return len(self.reverse_graph[v])
        except KeyError:
            return None

    def out_arcs(self, v):
        """
        returns the arcs leaving v
        """
        return self[v].values()
    
    out_edges = out_arcs

    def out_degree(self,v):
        """takes a vertex and returns the number of 
        arcs leaving it (the out-degree)"""
        try:
            return len(self[v])
        except KeyError:
            return None
    
    def add_all_arcs(self):
        """completes the graph by adding an arc from every vertex
        to every vertex"""
        for v in self.vertices():
            current_vertex = v
            for w in self.vertices():
                if current_vertex == w:
                    continue
                e = Arc(current_vertex,w)
                self.add_arc(e)
                
    add_all_edges = add_all_arcs
                
    def add_regular_arcs(self, k=2):
        """Make a regular directed graph with degree k if possible;
        otherwise raises an exception."""
        vs = self.vertices()
        if k >= len(vs):
            raise ValueError, ("cannot build a regular directed graph with " +
                               "degree >= number of vertices.")

        if (k % 2 == 1):
            raise ValueError, ("cannot build a regular directed graph with " +
                               "an odd degree")
        else:
            self._add_regular_arcs_even(k)

    def _add_regular_arcs_even(self, k=2):
        """
        Make a regular directed graph with degree k.  k must be even.
        """
        vs = self.vertices()
        double = vs * 2
        #FFFFFF
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_arc(Arc(v, w))

    def is_strongly_connected(self):
        """If the graph is strongly connected, returns True.
        Else, returns False."""
        def visit(v):
            self.visited_count += 1

        for v in self.vertices():
            v.visited = False
            
        for v in self.vertices():
            self.visited_count = 0
            for x in self.vertices():
                x.visited = False
            s = v

            self.bfs(s, visit = visit)

            if self.visited_count != len(self.vertices()):
                self.visited_count = None
                return False
        self.visited_count = None
        return True
                
    def is_complete(self):
        """checks if a graph is complete by ensuring that
        every vertex is adjacent to every other vertex in
        the graph"""
        for v in self.vertices():
            out_vertices = self.out_vertices(v)
            if len(out_vertices) != len(self.vertices())-1:
                return False
        return True
        
    def _cluster(self, v):
        """
        Helper function for DirectedGraph.clustering_coefficient.
        Calculates the clustering coefficient around a vertex v,
        and returns it.
        """
        es = 0.0
        neighbors = self[v].keys()
        neighbors.extend(self.reverse_graph[v].keys())

        for w in neighbors:
            for u in neighbors:
                try:
                    self[w][u]
                    es += 1.0
                except KeyError:
                    pass

        k = len(self[v]) + len(self.reverse_graph[v])
        try: 
            c = es / (k * (k-1))
        except ZeroDivisionError:
            try:
                c = es / (k * 1)
            except ZeroDivisionError:
                c = 0
        return c

    def clustering_coefficient(self):
        """Calculates the clustering coefficient for a graph,
        and returns it."""
        local_cs = [self._cluster(v) for v in self.keys()]
        c = sum(local_cs) / len(local_cs)

        return c
        
    def _bfsknots(self, s):
        """
        Modified breadth-first search. Used to find knots.Returns the 
        set of vertices that are accessible by some path from s.

        s: start vertex
        """

        # initialize the queue with the start vertex
        queue = [s]
        visited = set()
        on_first_vertex = True
        while queue:

            # get the next vertex
            v = queue.pop(0)

            # skip it if it's already marked
            if v in visited: continue

            # if we're on the first vertex, we're not actually visting
            if v != s or not on_first_vertex: visited.add(v)
            on_first_vertex = False
            
            for x in self.out_vertices(v):
                #if its out vertices have been cached, update visited
                if x in self._knot_cache.keys():
                    visited.update(self._knot_cache[x])
                    visited.add(x)
                    
                #otherwise add it to the queue
                elif x not in self._knot_cache.keys():
                    queue.append(x)

        return visited

    def _knot_at_v(self, v):
        """
        Given a vertex v, finds whether each of its out vertices
        are all accessible from each other, and not accessible from
        any other vertex.
        
        Returns True if this is case; indicates v is entrance to knot.
        """
        t = self._knot_cache.get(v, None)
        #print "Vertex: %s, Reachables: %s" %(str(v), str(t))
        if len(t) == 0:
            return False
            
        for w in self._knot_cache[v]:
                s = self._knot_cache.get(w, None)
                if len(s) == 0:
                    return False
                x = s.symmetric_difference(t)
                if x != set([]):
                    return False

        return True

    def has_knot(self):
        """
        Returns true if directed graph has a knot.
        """
        self._knot_cache = {}
        #build the cache of which vertices are accessible from which
        for v in self:
            self._knot_cache[v] = self._bfsknots(v)

        #searches for knot
        for v in self:
            if self._knot_at_v(v):
                return True
        return False

                
    def add_random_arcs(self, p=0.05):
        """Starting with an arcless graph, add arcs to
        form a random graph where (p) is the probability 
        that there is an arc between any pair of vertices.
        Follows the Erdos-Renyi model of a random graph.
        """
        vs = self.vertices()
        for i, v in enumerate(vs):
            for j, w in enumerate(vs):
                if v == w: continue
                if random.random() > p: continue
                self.add_arc(Arc(v, w))  
    


class WSDirectedGraph(DirectedGraph):
    def __init__(self,N,k,beta):
        """
        Creates a Watts-Strogatz Directed Graph
        starting with a k-regular graph with N vertices.
        Rewires the graph with probability beta.
        """
        if k % 2 == 1:
            raise ValueError, 'k must be even'
        vs = [Vertex(str(i)) for i in range(N)]
        DirectedGraph.__init__(self,vs,[])
        self.add_regular_arcs(k)
        self.rewire(beta)
        
    def rewire(self, p=0.01):
        """Rewires arcs according to the algorithm in Watts and Strogatz.
        (p) is the probability that each arc is rewired.
        """
        # consider the arcs in random order (this is slightly different
        # from Watts and Strogatz)
        es = list(self.arcs())
        random.shuffle(es)
        vs = self.vertices()
        
        for e in es:
            # if this arc is chosen, remove it...
            if random.random() > p: continue
            v, w = e
            self.remove_arc(v,w)

            # then generate a new arc that connects v to another vertex
            while True:
                w = random.choice(vs)
                if v is not w and not self.has_out_arc(v, w): break

            self.add_arc(Arc(v, w))    

class BADirectedGraph(DirectedGraph):
    """
    Represents a Small World Directed Graph, using the Barabasi-Albert
    algorithm to generate a small world graph.
    """
    def __init__(self, mo):      
        """
        @Args:
            mo, the initial number of vertices in the graph
        @Returns:
            None
        
        Creates a small world graph. Initializes the graph as a
        truly random Erdos-Renyi graph with a p of 0.5.
        """
        self.iter_labels = self._labels()
        vs = [Vertex(self.iter_labels.next()) for x in range(mo)]
        
        DirectedGraph.__init__(self, vs, [])
        self.mo = mo
        self.first_time_step()
        #~ self.add_all_arcs()
        self._initialize_histograms()
    
    def first_time_step(self):
        """
        We need to create as many initial edges as there are vertices, so we'll
        iterate through the number of vertices we need to create and connect
        two random non-identical vertices 
        """
        vs = self.vertices()
        edge_count = 0
        while edge_count < self.mo:
            v = random.choice(vs)
            w = random.choice(vs)
            if v == w:
                continue
            if self.has_arc(v,w):
                continue
            else:
                a = Arc(v,w)
                self.add_arc(a)
                edge_count += 1
        
    def _initialize_histograms(self):
        """
        @Args:
            None
        @Returns:
            None
        Creates two lists: node_in_histogram and node_out_histogram. These lists
        contain multiple copies of the same vertex, dependent on how many in
        and out arcs that vertex has. 
        """
        self._node_in_histogram = []
        self._node_out_histogram = []
        for v in self:
            #for every in arc a vertex has, add it to the node_in_histogram
            self._node_in_histogram.extend([v for i in range(self.in_degree(v))])
            #for eveyr out arc a vertex has, add it to the node_out_histogram
            self._node_out_histogram.extend([v for i in range(self.out_degree(v))])
            
    def single_time_step(self):
        """
        @Args:
            None
        @Returns:
            None
        Executes a single time step in a Barabasi-Albert Graph.
        """
        w = Vertex(self.iter_labels.next())
        self.add_vertex(w)
        #We add an equal number of in and out-arcs, so we need to check 
        #if the number of arcs we add is even or odd
        if self.mo % 2 == 1:
            m = self.mo - 1
        else:
            m = self.mo
            
        #Since the histograms contain more instances of vertices that are more
        #connected, if we randomly sample them, we'll get preferential 
        #attachment. Adapted from the NetworkX implementation of
        #Barabasi-Albert graphs.
        
        for v in random.sample(self._node_in_histogram, m/2):
            self.add_arc(Arc(w,v))
            self._node_in_histogram.append(v)
            
        for v in random.sample(self._node_out_histogram, m/2):
            self.add_arc(Arc(v,w))
            self._node_in_histogram.append(w)
            self._node_out_histogram.append(v)
            
        #We've created a bunch of out arcs from our new vertex,
        #so we need to add those arcs to our histogram.
        self._node_out_histogram.extend([w for i in range(m/2)])
        
        
    def build_graph(self,t):
        """
        @Args:
            t, the number of time steps to execute
        @Returns:
            None
        Builds the Barabasi-Albert Graph
        """
        for i in range(t):
            self.single_time_step()        
            
    def _labels(self):
        """
        Iterator that yields numerical labels for vertices
        """
        i = 0
        while True:
            yield str(i)
            i += 1

class LoopError(Exception):
    """
    Vertices cannot have Arcs leading to themselves. 
    So we throw an error.
    """
    
    def __init__(self, value):
        self.parameter = value
        
    def __str__(self):
        return repr(self.parameter)
        
class NotApplicableToDirectedGraphs(Exception):
    """
    Certain methods from Graph do not apply to DirectedGraph.
    So we throw an error.
    """
    
    def __init__(self, value):
        self.parameter = value
    
    def __str__(self):
        return repr(self.parameter)

def main(script,*args):
	v2 = Vertex('B')
	v1 = Vertex('A')
	a1 = Arc(v1,v2)
	dg = DirectedGraph([v2,v1],[a1])
	DirectedGraphWorld.show_directed_graph(dg)
    #~ dg = DirectedGraph(vs,[])
    #~ dg.add_all_edges()
    #~ swdg.build_graph(n)
    #~ dg = BADirectedGraph(30)
    #~ dg.build_graph(10)
    #~ DirectedGraphWorld.show_directed_graph(dg)

if __name__ == '__main__':
    import sys
    main(*sys.argv)

    
