""" Code example from Think Complexity, by Allen Downey.

Original code by Matt Aasted, modified by Allen Downey.

Based on Reynolds, "Flocks, Herds and Schools" and
Flake, "The Computational Beauty of Nature."

Copyright 2011 Allen B. Downey.
Distributed under the MIT License.
"""
try:
    from vpython import *
except:
    print("This program requires VPython 7, which you can read about")
    print("at http://vpython.org/.  If you are using Anaconda, you can")
    print("install VPython by running the following on the command line:")
    print("conda install -c vpython vpython")
    import sys
    sys.exit()

import numpy as np


null_vector = vector(0,0,0)


def random_vector(a, b):
    """Create a vector with each element uniformly distributed in [a, b)."""
    coords = np.random.uniform(a, b, size=3)
    return vector(*coords)


def limit_vector(vect):
    """If the magnitude is greater than 1, set it to 1"""
    if vect.mag > 1:
        vect.mag = 1
    return vect


class Boid(cone):
    """A Boid is a VPython cone with a velocity and an axis."""

    def __init__(self, radius=0.03, length=0.1):
        pos = random_vector(0, 1)
        self.vel = random_vector(0, 1).norm()
        cone.__init__(self, pos=pos, radius=radius, length=length)
        self.axis = length * self.vel

    def get_neighbors(self, boids, radius, angle):
        """Return a list of neighbors within a field of view.

        boids: list of boids
        radius: field of view radius
        angle: field of view angle in radians

        returns: list of Boid
        """
        neighbors = []
        for boid in boids:
            if boid is self:
                continue
            offset = boid.pos - self.pos

            # if not in range, skip it
            if offset.mag > radius:
                continue

            # if not within viewing angle, skip it
            diff = self.vel.diff_angle(offset)
            if abs(diff) > angle:
                continue

            # otherwise add it to the list
            neighbors.append(boid)

        return neighbors

    def center(self, boids, radius=1, angle=1):
        """Find the center of mass of other boids in range and
        return a vector pointing toward it."""
        neighbors = self.get_neighbors(boids, radius, angle)
        vecs = [boid.pos for boid in neighbors]
        return self.vector_toward_center(vecs)

    def vector_toward_center(self, vecs):
        """Vector from self to the mean of vecs.

        vecs: sequence of vector

        returns: Vector
        """
        if vecs:
            center = np.mean(vecs)
            toward = vector(center - self.pos)
            return limit_vector(toward)
        else:
            return null_vector

    def avoid(self, boids, carrot, radius=0.3, angle=np.pi):
        """Find the center of mass of all objects in range and
        return a vector in the opposite direction, with magnitude
        proportional to the inverse of the distance (up to a limit)."""
        objects = boids + [carrot]
        neighbors = self.get_neighbors(objects, radius, angle)
        vecs = [boid.pos for boid in neighbors]
        return -self.vector_toward_center(vecs)

    def align(self, boids, radius=0.5, angle=1):
        """Return the average heading of other boids in range.

        boids: list of Boids
        """
        neighbors = self.get_neighbors(boids, radius, angle)
        vecs = [boid.vel for boid in neighbors]
        return self.vector_toward_center(vecs)

    def love(self, carrot):
        """Returns a vector pointing toward the carrot."""
        toward = carrot.pos - self.pos
        return limit_vector(toward)

    def set_goal(self, boids, carrot):
        """Sets the goal to be the weighted sum of the goal vectors."""

        # weights for various rules
        w_avoid = 10
        w_center = 3
        w_align = 1
        w_love = 10

        self.goal = (w_center * self.center(boids) +
                     w_avoid * self.avoid(boids, carrot) +
                     w_align * self.align(boids) +
                     w_love * self.love(carrot))
        self.goal.mag = 1

    def move(self, mu=0.1, dt=0.1):
        """Update the velocity, position and axis vectors.

        mu: how fast the boids can turn (maneuverability).
        dt: time step
        """

        self.vel = (1-mu) * self.vel + mu * self.goal
        self.vel.mag = 1
        self.pos += dt * self.vel
        self.axis = self.length * self.vel


class World(object):

    def __init__(self, n=10):
        """Create n Boids and one carrot.

        tracking: indicates whether the carrot follows the mouse
        """
        self.boids = [Boid() for i in range(n)]
        self.carrot = sphere(pos=vector(1,0,0),
                             radius=0.1,
                             color=vector(1,0,0))
        self.tracking = False

    def step(self):
        """Compute one time step."""
        # move the boids
        for boid in self.boids:
            boid.set_goal(self.boids, self.carrot)
            boid.move()

        # if we're tracking, move the carrot
        if self.tracking:
            self.carrot.pos = scene.mouse.pos


n = 20
size = 5

world = World(n)
scene.center = world.carrot.pos
scene.autoscale = False

def toggle_tracking(evt):
    """If we're currently tracking, turn it off, and vice versa.
    """
    world.tracking = not world.tracking

# when the user clicks, toggle tracking.
scene.bind('click', toggle_tracking)

while 1:
    rate(10)
    world.step()
