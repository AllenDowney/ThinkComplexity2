""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2016 Allen Downey
MIT License: http://opensource.org/licenses/MIT
"""

import matplotlib.pyplot as plt
from matplotlib import animation


def animate(model, frames=None, interval=1, step=None):
    """Animates a Cell2D model in a Matplotlib window.

    Cell2D.animate is meant for notebooks; this does the same job
    in a script.  Keep a reference to the result until plt.show()
    returns, or the animation is garbage collected.

    model: Cell2D object
    frames: number of frames to draw, or None to run until the window closes
    interval: time between frames in milliseconds
    step: function that advances the model one frame (default: model.step)

    returns: FuncAnimation
    """
    if step is None:
        step = model.step

    fig = plt.figure()

    def update(i):
        if i > 0:
            step()
        plt.cla()
        model.draw()

    return animation.FuncAnimation(fig, update, frames=frames,
                                   interval=interval, repeat=False,
                                   cache_frame_data=False)
