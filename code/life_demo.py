""" Code example from Think Complexity, by Allen Downey.

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d

def add_cells(x, y, *strings):
    """Adds cells at the given location.
    
    x: left coordinate
    y: top coordinate
    strings: list of strings of 0s and 1s
    """
    for i, s in enumerate(strings):
        a[y+i, x:x+len(s)] = np.array([int(b) for b in s])

# the starting patterns
lwss = [
    '0001',
    '00001',
    '10001',
    '01111'
]

bhep = [
    '1',
    '011',
    '001',
    '001',
    '01'
]

# add up the neighbors and get 10 points if the middle is live
kernel = np.array([[1, 1, 1],
                   [1,10, 1],
                   [1, 1, 1]], dtype=np.uint8)

# the cell is live if the total is 3, 12, or 13
table = np.zeros(20, dtype=np.uint8)
table[[3, 12, 13]] = 1

# make the array
n = 200
m = 600
a = np.zeros((n, m), np.uint8)

# add the initial patterns
x = 100
add_cells(x, n//2-8, *lwss)
add_cells(x, n//2+6, *lwss)
add_cells(x, n//2-1, *bhep)

# draw the initial state
fig = plt.figure()
cmap = plt.get_cmap('Greens')
im = plt.imshow(a, cmap=cmap, interpolation='nearest')
plt.xticks([])
plt.yticks([])

# animate the rest
def animate_func(i):
    """Draws one frame of the animation."""
    global a
    c = convolve2d(a, kernel, mode='same')
    a = table[c]
    im.set_array(a)
    return im,

anim = animation.FuncAnimation(fig, animate_func, frames=100, interval=0)
plt.show()
