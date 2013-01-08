""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

from Graph import Vertex, Edge, Graph


class Tests(unittest.TestCase):

    def test_graph(self):
        v = Vertex('v')
        w = Vertex('w')
        self.assertEqual(repr(v), "Vertex('v')")

        e = Edge(v, w)
        self.assertEqual(repr(e), "Edge(Vertex('v'), Vertex('w'))")

        g = Graph([v,w], [e])
        self.assertEqual(repr(g), "{Vertex('w'): {Vertex('v'): Edge(Vertex('v'), Vertex('w'))}, Vertex('v'): {Vertex('w'): Edge(Vertex('v'), Vertex('w'))}}")

        e2 = g.get_edge(v, w)
        self.assertEqual(e, e2)

        e3 = g.get_edge(v, v)
        self.assertEqual(e3, None)

        vs = [Vertex(c) for c in 'abcd']
        g = Graph(vs)
        g.add_regular_edges(3)

        for v in g.vertices():
            es = g.out_edges(v)
            self.assertEqual(len(es), 3)

            vs = g.out_vertices(v)
            self.assertEqual(len(vs), 3)

        g.remove_edge(Edge(Vertex('a'), Vertex('c')))

        vs = g.vertices()
        self.assertEqual(len(vs), 4)

        es = g.edges()
        self.assertEqual(len(es), 5)

        g.add_all_edges()
        es = g.edges()
        self.assertEqual(len(es), 6)

        g2 = eval(repr(g))
        self.assertEqual(g, g2)


if __name__ == '__main__':
    unittest.main()
