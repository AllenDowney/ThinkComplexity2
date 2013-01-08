""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

class Callable(object):
    """Wrap a function and its arguments in a callable object.

    Callables can can be passed as a callback parameter and invoked later.

    This code is adapted from the Python Cookbook 9.1, page 302,
    with one change: if call is invoked with args and kwds, they
    are added to the args and kwds stored in the Callable.
    """
    def __init__(self, func, *args, **kwds):
        self.func = func
        self.args = args
        self.kwds = kwds

    def __call__(self, *args, **kwds):
        d = dict(self.kwds)
        d.update(kwds)
        return apply(self.func, self.args+args, d)

    def __str__(self):
        return self.func.__name__


