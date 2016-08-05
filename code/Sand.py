import itertools

import numpy as np
import matplotlib.pyplot as plt

from Cell2D import Cell2D, Cell2DViewer
from scipy.signal import correlate2d


class SandPile(Cell2D):
    """Diffusion Cellular Automaton."""

    kernel = np.array([[0, 1, 0],
                       [1,-4, 1],
                       [0, 1, 0]], dtype=np.int32)

    def __init__(self, n, m=None):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        r: diffusion rate constant
        """
        m = n if m is None else m
        choices = np.array([2, 3, 4], dtype=np.int32)
        self.array = np.random.choice(choices, (n, m))
        self.total = np.zeros((n, m), dtype=np.int32)
        self.swept_seq = []
        self.toppled_seq = []

    def step(self, K=4):
        """Executes one time step.
        
        returns: number of cells that toppled
        """
        a = self.array
        n, m = a.shape
        
        toppling = a>K
        self.total += toppling
        
        num_toppled = np.sum(toppling)
        c = correlate2d(toppling, self.kernel, mode='same')
        self.array += c
        return num_toppled
    
    def sweep(self):
        """Sweeps the edges.
        
        returns: total of all swept cells
        """
        a = self.array
        total = np.sum(a[[0, -1]]) + np.sum(a[:, [0, -1]])
        a[[0, -1]] = 0
        a[:, [0, -1]] = 0
        return total
    
    def drop(self):
        """Increments a random cell."""
        a = self.array
        n, m = a.shape
        index = np.random.randint(n), np.random.randint(m)
        a[index] += 1
    
    def run(self):
        """Runs until equilibrium.
        
        returns: duration, total number of topplings
        """
        total = 0
        for i in itertools.count(1):
            swept = self.sweep()
            toppled = self.step()

            self.swept_seq.append(swept)
            self.toppled_seq.append(toppled)
            
            total += toppled
            if toppled == 0:
                return i, total
            
    def drop_and_run(self):
        """Drops a random grain and runs to equilibrium.
        
        returns: duration, swept, toppled
        """
        self.drop()
        duration, toppled = self.run()
        return duration, toppled


class SandPileViewer(Cell2DViewer):
    cmap = plt.get_cmap('YlOrRd')
    options = dict(interpolation='none', alpha=0.8,
                   vmin=0, vmax=7)
    
#    def step(self, iters=1):
#        """Advances the viewee the given number of steps."""
#        for i in range(iters):
#            self.viewee.drop_and_run()
            
    def draw_total(self, mod_flag=False):
        cmap = plt.get_cmap('YlOrRd')
        options = dict(interpolation='none', alpha=0.8)
        if mod_flag:
            a = self.viewee.total % 2
        else:
            a = self.viewee.total
            
        self.draw_array(a, cmap, **options)


def tower(pile, factor=2):
    a = pile.array
    n, m = a.shape
    
    a[:, :] = 0
    a[n//2, m//2] = factor * n * m



def main():
    n = 100
    pile = SandPile(n)
    tower(pile)
    viewer = SandPileViewer(pile)
    anim = viewer.animate(interval=0)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()

if __name__ == '__main__':
    main()
