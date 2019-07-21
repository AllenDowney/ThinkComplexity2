from pylab import *
from CellWorld import *
from cmath import *
from Fourier import fft
from Dist import *        

class Forest(CellWorld):
    """Forest implements a CA model of a forest fire, as described
    at http://en.wikipedia.org/wiki/Forest-fire_model
    """

    def __init__(self, size=500, csize=5, p=0.01, f=0.001):
        CellWorld.__init__(self, size, csize)
        self.p = p              # probability of a new tree
        self.f = f              # probability of a spontaneous fire
        self.series = []
        
    def setup(self):
        # the left frame contains the canvas
        self.fr(LEFT)
        self.canvas = self.ca(width=self.size, height=self.size,
                              bg='white', scale = [self.csize, self.csize])
        self.endfr()

        # the right frame contains various buttons
        self.fr(LEFT, fill=BOTH, expand=1)

        self.fr()
        self.bu(LEFT, text='Print canvas', command=self.canvas.dump)
        self.bu(LEFT, text='Quit', command=self.quit)
        self.endfr()

        self.fr()
        self.bu(LEFT, text='Run', command=self.run)
        self.bu(LEFT, text='Stop', command=self.stop)
        self.bu(LEFT, text='Step', command=self.profile_step)
        self.endfr()

        self.fr()
        self.bu(LEFT, text='Show clusters', command=self.cluster_dist)
        self.endfr()

        self.endfr()

        # make a grid of cells
        xbound = self.size / self.csize / 2 -1
        ybound = xbound
        low = [-xbound, -ybound]
        high = [xbound, ybound]
        self.make_cells([low, high])

    def make_cells(self, limits):
        """make a grid of cells with the specified limits.
        limits is a list of pairs, [[lowx, lowy], [highx, highy]]"""
        low, high = limits
        xs = range(low[0], high[0])
        ys = range(low[1], high[1])
        for x in xs:
            col = []
            for y in ys:
                indices = (x, y)
                self.cells[indices] = Patch(self, indices)

    def get_cluster(self, patch):
        """find the set of cells that are connected to (patch) in
        the sense that they are either neighbors, or neighbors of
        neighbors, etc.
        """

        # queue is the set of cells waiting to be checked
        queue = set([patch])

        # res it the resulting set of cells
        res = set([patch])

        # do a breadth first search based on neighbors relationships
        while queue:
            patch = queue.pop()
            neighbors = self.get_four_neighbors(patch, Patch.null)

            # look for green neighbors we haven't seen before
            new = [n for n in neighbors
                   if n.state == 'green' and n not in res]

            # and add them to the cluster
            queue.update(new)
            res.update(new)
            
        return res

    def all_clusters(self):
        """find all the clusters in the current grid (returns a list
        of sets).
        """

        # find all the green cells
        greens = [p for p in self.cells.itervalues() if p.state == 'green']

        # keep track of cells we have already seen
        marked = set()

        # initialize the list of cluster
        clusters = []
        
        for patch in greens:
            if patch in marked: continue
            cluster = self.get_cluster(patch)

            # add the new cluster to the list
            clusters.append(cluster)

            # and mark the cells in the cluster
            marked.update(cluster)

        return clusters

    def cluster_dist(self):
        """compute and display the distribution of cluster sizes.
        """
        clusters = self.all_clusters()
        lengths = [len(cluster) for cluster in clusters]
        d = Dist(lengths)
        d.plot_ccdf(loglog)
        show()
    
    def bind(self):
        """create bindings for the canvas
        """
        self.canvas.bind('<ButtonPress-1>', self.click)

    def click(self, event):
        """this event handler is executed when the user clicks on
        the canvas.  It finds the cluster of the cell that was clicked
        and displays it in red.
        """
        x, y = self.canvas.invert([event.x, event.y])
        i, j = int(floor(x)), int(floor(y))
        patch = self.get_cell(i,j)
        if patch and patch.state == 'green':
            cluster = self.get_cluster(patch)
            self.show_cluster(cluster)

    def show_cluster(self, cluster):
        """color all the cells in this cluster red
        """
        for patch in cluster:
            patch.config(fill='red')

    def profile_step(self):
        """run one step and profile it
        """
        import profile
        profile.run('world.step()')

    def step(self):
        """run one step: update the cells, counting the number
        that are burning.  Update the time series and display
        the its FFT.
        """
        burning = 0
        for patch in self.cells.itervalues():
            patch.step()
            if patch.state == 'orange':
                burning += 1

        self.series.append(burning)
        self.display_fft(256)

    def display_fft(self, N=4096):
        """display the FFT of the last (N) values in self.series
        """
        if len(self.series) % N != 0:
            return

        h = self.series[-N:]
        H = fft(h)

        # the squared magnitude of the fft is an estimate of the
        # power spectral density

        # http://documents.wolfram.com/applications/timeseries/
        #      UsersGuidetoTimeSeries/1.8.3.html
        # http://en.wikipedia.org/wiki/Power_spectral_density
        freq = range(N/2 + 1)
        sdf = [Hn * Hn.conjugate() for Hn in H]
        sdf = [sdf[f].real for f in freq]
        loglog(freq, sdf)
        xlabel('frequency')
        ylabel('power')
        show()

        
class Patch(Cell):
    """a Patch is a part of a forest that may or may not have one tree
    """
    def __init__(self, world, indices):
        """world is a Forest, indices is a tuple of integer coordinates
        """
        self.world = world
        self.indices = indices
        self.bounds = self.world.cell_bounds(*indices)
        self.state = 'white'
        self.draw()

    def draw(self):
        """draw this patch
        """
        coords = self.bounds[::2]
        self.tag = self.world.canvas.rectangle(coords,
                                 outline='gray80', fill=self.state)
        
    def set_state(self, state):
        """set the state of this patch and update the display.
        (state) must be a color.
        """
        self.state = state
        self.config(fill=self.state)
        
    def step(self):
        """update this patch
        """
        # invoke the appropriate function, according to self.state
        Patch.dispatch[self.state](self)
        
    def step_empty(self):
        """update an empty patch
        """
        if random.random() < self.world.p:
            self.set_state('green')

    def step_tree(self):
        """update a patch with a tree
        """
        if random.random() < self.world.f or self.any_neighbor_burning():
            self.set_state('orange')

    def step_burning(self):
        """update a burning patch
        """
        self.set_state('white')

    dispatch = dict(white=step_empty, green=step_tree, orange=step_burning)

    class NullPatch:
        """the NullPatch is a singleton that acts as a stand-in for
        non-existent patches
        """
        def __init__(self):
            self.state = 'white'

    # instantiate the null patch
    null = NullPatch()

    def any_neighbor_burning(self):
        """return True if any of this patch's 4 Von Neumann neighbors
        are currently burning, False otherwise.
        """
        neighbors = self.world.get_four_neighbors(self, Patch.null)
        states = [patch.state for patch in neighbors]
        return 'orange' in states


if __name__ == '__main__':
    world = Forest()
    world.bind()
    world.mainloop()
