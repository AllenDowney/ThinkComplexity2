from CellWorld import *

class Forest(TurmiteWorld):

    def __init__(self, p=0.01, f=0.001):
        World.__init__(self)
        self.delay = 0.0        # time in seconds to sleep after an update
        self.ca_width = 500     # canvas width and height
        self.ca_height = 500
        self.csize = 5          # cell size in pixels
        self.cells = {}         # a dictionary that maps coordinates to cells
        self.p = p              # probability of a new tree
        self.f = f              # probability of a spontaneous fire
        self.setup()
        
    def setup(self):

        # the left frame contains the canvas
        self.fr(LEFT)
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white')
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
        self.bu(LEFT, text='Step', command=self.step)
        self.bu(LEFT, text='Clear', command=self.clear)
        self.endfr()

        self.endfr()

        low = [-40, -40]
        high = [40, 40]
        self.make_cells([low, high])

    def make_cells(self, limits):
        """make a grid of cells with the specified limits.
        limits is a list of pairs, [[lowx, lowy], [highx, highy]]"""
        low, high = limits
        for x in range(low[0], high[0]):
            col = []
            for y in range(low[1], high[1]):
                indices = (x, y)
                self.cells[x,y] = Patch(self, indices)

    def step(self):
        for cell in self.cells.itervalues():
            cell.step()

class Patch(Cell):
    """a patch is a part of a forest that may or may not have one tree
    """
    def __init__(self, world, indices):
        self.world = world
        self.indices = indices
        bounds = world.cell_bounds(*indices)
        self.tag = world.canvas.polygon(bounds, outline='gray80')
        self.mark_empty()

    def mark_empty(self):
        self.state = 0
        self.config_cell(fill='white')

    def mark_tree(self):
        self.state = 1
        self.config_cell(fill='green')

    def mark_burning(self):
        self.state = 2
        self.config_cell(fill='orange')

    def step(self):
        """advance this patch in time by one step"""
        pass


if __name__ == '__main__':
    world = Forest()
    world.mainloop()
