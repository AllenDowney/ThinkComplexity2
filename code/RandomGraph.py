""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import string
import random

from collections import deque

from Graph import *


class RandomGraph(Graph):
    """An Erdos-Renyi random graph is a Graph where the probability 
    of an edge between any two nodes is (p).
    """

    def add_random_edges(self, p=0.05):
        """Starting with an edgeless graph, add edges to
        form a random graph where (p) is the probability 
        that there is an edge between any pair of vertices.
        """
        vs = self.vertices()
        for i, v in enumerate(vs):
            for j, w in enumerate(vs):
                if j <= i: continue
                if random.random() > p: continue
                self.add_edge(Edge(v, w))


    def bfs(self, s, visit=None):
        """Breadth first search, starting with (s).
        If (visit) is provided, it is invoked on each vertex.
        Returns the set of visited vertices.
        """
        visited = set()

        # initialize the queue with the start vertex
        queue = deque([s])
        
        # loop until the queue is empty
        while queue:

            # get the next vertex
            v = queue.popleft()

            # skip it if it's already visited
            if v in visited: continue

            # mark it visited, then invoke the visit function
            visited.add(v)
            if visit: visit(v)

            # add its out vertices to the queue
            queue.extend(self.out_vertices(v))

        # return the visited vertices
        return visited

    def is_connected(self):
        """Returns True if there is a path from any vertex to
        any other vertex in this graph; False otherwise.
        """
        vs = self.vertices()
        visited = self.bfs(vs[0])
        return len(visited) == len(vs)


def show_graph(g):
    import GraphWorld

    for v in g.vertices():
        if v.visited: 
            v.color = 'white'
        else:
            v.color = 'red'

    layout = GraphWorld.CircleLayout(g)
    gw = GraphWorld.GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()


def test_graph(n, p):
    """Generates a random graph with (n) vertices and probability (p).
    Returns True if it is connected, False otherwise
    """
    labels = string.lowercase + string.uppercase + string.punctuation
    vs = [Vertex(c) for c in labels[:n]]
    g = RandomGraph(vs)
    g.add_random_edges(p=p)
    # show_graph(g)
    return g.is_connected()


def test_p(n, p, num):
    """Generates (num) random graphs with (n) vertices and
    probability (p) and return the count of how many are connected.
    """
    count = 0
    for i in range(num):
        if test_graph(n, p):
            count += 1
    return count


def main(script, n=26, p=0.1, num=1, *args):
    n = int(n)
    p = float(p)
    num = int(num)
    count = test_p(n, p, num)
    print count


if __name__ == '__main__':
    import sys
    main(*sys.argv)
