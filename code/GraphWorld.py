""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import string
import random
import math

from itertools import chain

try:
    from Gui import Gui, GuiCanvas
except ImportError:
    from swampy.Gui import Gui, GuiCanvas

from Graph import Vertex
from Graph import Edge
from Graph import Graph


class GraphCanvas(GuiCanvas):
    """a GraphCanvas is a canvas that knows how to draw Vertices
    and Edges"""

    def draw_vertex(self, v, r=0.45):
        """draw a Vertex as a yellow circle with radius (r)
        and text (v.label)"""
        tag = 'v%d' % id(self)

        try:
            color = v.color
        except:
            color = 'yellow'

        self.circle(v.pos, r, color, tags=tag)
        self.text(v.pos, v.label, 'black', tags=tag)
        return tag

    def draw_edge(self, e):
        """draw an Edge as a line between the positions of the
        Vertices it connects"""
        v, w = e
        tag = self.line([v.pos, w.pos])
        return tag


class GraphWorld(Gui):
    """GraphWorld is a Gui that has a Graph Canvas and control buttons."""
    
    def __init__(self):
        Gui.__init__(self)
        self.title('GraphWorld')
        self.setup()

    def setup(self):
        """Create the widgets."""
        self.ca_width = 400
        self.ca_height = 400
        xscale = self.ca_width / 20
        yscale = self.ca_height / 20

        # canvas
        self.col()
        self.canvas = self.widget(GraphCanvas, scale=[xscale, yscale],
                              width=self.ca_width, height=self.ca_height,
                              bg='white')
        
        # buttons
        self.row()
        self.bu(text='Clear', command=self.clear)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

    def show_graph(self, g, layout):
        """Draws the Vertices and Edges of Graph (g) using the
        positions in Layout (layout).
        """

        # copy the positions from the layout into the Vertex objects
        for v in g.vertices():
            v.pos = layout.pos(v)
        
        # draw the edges and store the tags in self.etags, which maps
        # from Edges to their tags
        c = self.canvas
        self.etags = {}
        for v in g:
            self.etags[v] = [c.draw_edge(e) for e in g.out_edges(v)]

        # draw the vertices and store their tags in a list
        self.vtags = [c.draw_vertex(v) for v in g]

    def clear(self):
        """Delete all canvas items."""
        tags = chain(self.vtags, *self.etags.itervalues())
        for tag in tags:
            self.canvas.delete(tag)


class Layout(dict):
    """A Layout is a mapping from vertices to positions in 2-D space."""

    def __init__(self, g):
        for v in g.vertices():
            self[v] = (0, 0)

    def pos(self, v):
        """Returns the position of this Vertex as a tuple."""
        return self[v]

    def distance_between(self, v1, v2):
        """Computes the Euclidean distance between two vertices."""
        x1, y1 = self.pos(v1)
        x2, y2 = self.pos(v2)
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx**2 + dy**2)

    def sort_by_distance(self, v, others):
        """Returns a list of the vertices in others sorted in
        increasing order by their distance from v."""
        t = [(self.distance_between(v, w), w) for w in others]
        t.sort()
        return [w for (d, w) in t]


class CircleLayout(Layout):
    """Creates a layout for a graph with the vertices equally
    spaced around the perimeter of a circle."""

    def __init__(self, g, radius=9):
        """Creates a layout for Graph (g)"""
        vs = g.vertices()
        theta = math.pi * 2 / len(vs)
        for i, v in enumerate(vs):
            x = radius * math.cos(i * theta)
            y = radius * math.sin(i * theta)
            self[v] = (x, y)


class RandomLayout(Layout):
    """Create a layout with each Vertex at a random position in
    [[-max, -max], [max, max]]."""

    def __init__(self, g, max=10):
        """Creates a layout for Graph (g)"""
        self.max = max
        for v in g.vertices():
            self[v] = self.random_pos()

    def random_pos(self):
        """choose a random position and return it as a tuple"""
        x = random.uniform(-self.max, self.max)
        y = random.uniform(-self.max, self.max)
        return x, y

    def spread_vertex(self, v, others, min_dist=1.0):
        """Keep choosing random positions for v until it is at least
        min_dist units from the vertices in others.

        Each time it fails, it relaxes min_dist by 10%.
        """
        while True:
            t = [(self.distance_between(v, w), w) for w in others]
            d, w = min(t)
            if d > min_dist:
                break
            min_dist *= 0.9
            self[v] = self.random_pos()

    def spread_vertices(self):
        """Moves the vertices around until no two are closer together
        than a minimum distance."""
        vs = self.keys()
        others = vs[:]
        for v in vs:
            others.remove(v)
            self.spread_vertex(v, others)
            others.append(v)



def main(script, n='10', *args):

    # create n Vertices
    n = int(n)
    labels = string.ascii_lowercase + string.ascii_uppercase
    vs = [Vertex(c) for c in labels[:n]]

    # create a graph and a layout
    g = Graph(vs)
    g.add_all_edges()
    layout = CircleLayout(g)

    # draw the graph
    gw = GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()


if __name__ == '__main__':
    import sys
    main(*sys.argv)


