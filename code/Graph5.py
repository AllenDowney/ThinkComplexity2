"""Make a random graph with preferential attachment
(as described in Barabasi et al, Emergence of Scaling
in Random Networks), and plot the distribution of
node degrees.
"""
from Graph import *
from Dist import Dist

# make the initial graph
v1 = Vertex()
v2 = Vertex()
e = Edge(v1, v2)
g = Graph([v1, v2], [e])


# add new vertices and edges
for i in range(2000):
    v1 = Vertex()
    v2 = g.random_vertex()
    e = Edge(v1, v2)
    g.add_vertex(v1)
    g.add_edge(e)


# plot the histogram of degrees
d = Dist()
vs = g.vertices()
for v in vs:
    d.count(v.degree)


d.plot_ccdf(loglog)
show()

