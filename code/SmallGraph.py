    def add_local_edges(self, layout, k=3):
        """
        Note that some Vertices may have more than (k) edges because
        k-closest is not a symmetric relationship.
        """
        vs = self.vertices()
        others = vs[:]
        for v in vs:
            others.remove(v)
            t = layout.sort_by_distance(v, others)
            for w in t[:k]:
                self.add_edge(Edge(v,w))
            others.append(v)
