import string
from Graph import *
from SmallWorldGraph import *
from GraphWorld import *


def make_sw_graph(n=52, k=10, p=0.1):
    """make a small world graph according to the algorithm in Watts
    and Strogatz.  (n) is the number of vertices, (k) is the number
    of neighbors each Vertex is connected to, (p) is the probability
    of rewiring an edge.  (k) must be even.

    Compute and return the characteristic length (cl) and the
    clustering coefficient (cc).
    """
    names = name_generator()
    vs = [Vertex(names.next()) for i in range(n)]
    g = SmallWorldGraph(vs)

    g.add_regular_edges(k=k)
    g.rewire(p=p)

    cl = g.char_length()
    cc = g.cluster_coef()

    return cl, cc

def estimate_cl_cc(n=52, k=10, p=0.1, runs=3):
    """generate (runs) small world graphs with the given parameters
    and return the average characteristic length and cluster coefficient.
    """
    data = [make_sw_graph(n, k, p) for i in range(runs)]
    cls, ccs = zip(*data)
    return avg(cls), avg(ccs)

def estimate_cls_ccs(n=52, k=10, ps=[0.1], runs=3):
    """loop through the values of (p) in (ps) and print the
    estimated characteristic length and cluster coefficient.
    """
    for p in ps:
        ls, cs = estimate_cl_cc(n, k, p, runs)
        print p, ls, cs



ps = [0, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]

estimate_cls_ccs(n=200, k=10, ps=ps, runs=1)

#import profile
#ps = [1e-3]
#cmd = 'estimate_cls(n=200, k=10, ps=ps, runs=3)'
#profile.run(cmd)

