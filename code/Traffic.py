
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

from Highway import *

class BadDriver(Driver):
    def choose_speed(self, dist):
        """adjust the speed of the Driver according to the following
        distance."""

        # if there's enough space, speed up; otherwise, slow down
        if dist > 50:
            self.speed += 1
        else:
            self.speed -= 3

        # can't go backward; can't exceed the speed limit
        self.speed = max(self.speed, 0)
        self.speed = min(self.speed, 10)
  
def main(script, n=50):
    n = int(n)
    make_highway(n, BadDriver)

if __name__ == '__main__':
    import sys
    main(*sys.argv)
