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

    def __init__(self, n, m=None, level=9):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        level: starting value for all cells
        """
        m = n if m is None else m
        self.array = np.ones((n, m), dtype=np.int32) * level
        self.reset()

    def reset(self):
        """Start keeping track of the number of toppled cells.
        """
        self.toppled_seq = []

    def step(self, K=3):
        """Executes one time step.
        
        returns: number of cells that toppled
        """
        toppling = self.array > K
        num_toppled = np.sum(toppling)
        self.toppled_seq.append(num_toppled)

        c = correlate2d(toppling, self.kernel, mode='same')
        self.array += c
        return num_toppled
    
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
            num_toppled = self.step()
            total += num_toppled
            if num_toppled == 0:
                return i, total

    def drop_and_run(self):
        """Drops a random grain and runs to equilibrium.
        
        returns: duration, total_toppled
        """
        self.drop()
        duration, total_toppled = self.run()
        return duration, total_toppled


class SandPileViewer(Cell2DViewer):
    cmap = plt.get_cmap('YlOrRd')
    options = dict(interpolation='nearest', alpha=0.8,
                   vmin=0, vmax=5)
    
    def __init__(self, viewee, drop_flag=True):
        """Initializes the attributes.

        drop_flag: determines whether `step` drops a grain
        """
        Cell2DViewer.__init__(self, viewee)
        self.drop_flag = drop_flag

    def step(self):
        """Advances the viewee one step."""
        if self.drop_flag:
            self.viewee.drop_and_run()
        else:
            self.viewee.step()


def single_source(pile, height=1024):
    """Adds a tower to the center cell.
    
    height: value assigned to the center cell
    """
    a = pile.array
    n, m = a.shape
    a[:, :] = 0
    a[n//2, m//2] = height


def main():
    n = 101
    pile = SandPile(n)
    single_source(pile, height=2**14)
    viewer = SandPileViewer(pile, drop_flag=False)
    anim = viewer.animate(interval=0)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.show()


if __name__ == '__main__':
    main()
