""" Reimplementation of model of ant trails by Deneuborg et al., 1989.

Call this program from the command line like this:
python ants.py timesteps

...where timesteps is an integer that represents the number of time
steps for which the simulation should run.

Copyright 2011 Chloe Vilain and Andrew Pikler.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import random
import wx
import math
import sys
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas

class Ant:
	"""A single Ant in the World."""
		
	def __init__(self, world):
		"""world is a reference to the World object."""
		self.world = world
		self.x = 0
		self.y = 0
		self.has_food = 0
		
	def getPos(self):
		"""Returns the (x, y) position of this Ant as a tuple."""
		return (self.x, self.y)
	
	def setPos(self, pos):
		"""Sets the (x, y) position of this Ant to pos."""
		self.x = pos[0]
		self.y = pos[1]
	
	def next_left(self):
		"""Returns the (x, y) position of the Location the Ant 
		would move to if it moved forward left.
		"""
		if not self.has_food:
			return (self.x, self.y + 1)
		else:
			return (self.x, self.y - 1)
	
	def next_right(self):
		"""Returns the (x, y) position of the Location the Ant 
		would move to if it moved forward right.
		"""
		if not self.has_food:
			return (self.x + 1, self.y)
		else:
			return (self.x - 1, self.y)
	
	def left_pheromone(self):
		"""Returns the amount of pheromone in the Location that 
		the Ant	would move into if it moved forward left.
		"""
		return self.world.get_pheromone(self.next_left())
	
	def right_pheromone(self):
		"""Returns the amount of pheromone in the Location that 
		the Ant	would move into if it moved forward right.
		"""
		return self.world.get_pheromone(self.next_right())
	
	def will_move(self):
		"""Returns whether or not this Ant will move this turn."""
		if self.world.at_capacity(self.next_left()) and \
			self.world.at_capacity(self.next_right()):
			return False
		p_l = self.left_pheromone()
		p_r = self.right_pheromone()
		prob_move = 0.5 + 0.5*math.tanh((p_l + p_r) / 100.0 - 1)
		return random.random() < prob_move

	def will_go_right(self):
		"""Returns whether or not this Ant will move forward right
		this turn.
		"""
		p_l = self.left_pheromone()
		p_r = self.right_pheromone()

		if self.world.at_capacity(self.next_right()):
			return False

		if self.world.at_capacity(self.next_left()):
			return True

		prob_right = (1 - (5 + p_l)**2 / 
			      float((5 + p_l)**2 + (5 + p_r)**2))

		return random.random() < prob_right
		
	def move(self):
		"""Moves this Ant."""
		if not self.will_move(): 
			return
		if self.will_go_right():
			self.setPos(self.next_right())
		else:
			self.setPos(self.next_left())
		self.lay_pheromone()
		pos = self.getPos()
		if pos == (0, 0):
			self.has_food = False
		else:
			if self.world.has_food(pos) and not self.has_food:
				self.world.remove_food(pos)
				self.has_food = True

	def lay_pheromone(self):
		"""This Ant lays pheromone in its current Location."""
		pos = self.getPos()
		current = self.world.get_pheromone(pos)
		if not self.has_food:
			limit = 1000
			amount = 1
		else:
			limit = 300
			amount = 10
		if current >= limit: 
			return
		new_amount = min(current + amount, limit)
		self.world.set_pheromone(pos, new_amount)

class Location:
	"""A discrete point on the map. Can contain food and pheromone."""
	
	def __init__(self):
		self.food = 0
		self.pheromone = 0
		
	def place_food(self, p):
		"""Place food with probability p into this Location."""
		if random.random() < p:
			self.food = 1

	def has_food(self):
		"""Returns True if this Location has at least 1 food in it,
		False otherwise.
		"""
		return self.food > 0
	
	def remove_food(self):
		"""Remove one food from this Location. Crashes if there is
		no food in this Location.
		"""
		assert(self.has_food)
		self.food -= 1
	
	def add_pheromone(self, amount=1):
		"""Add pheromone to this Location."""
		self.pheromone += amount
	
	def set_pheromone(self, amount):
		"""Set the pheromone in this Location to amount."""
		self.pheromone = amount
	
	def get_pheromone(self):
		"""Returns the amount of pheromone in this Location."""
		return self.pheromone
		
	def evaporate_pheromone(self):
		"""Evaporates 1/30 of the pheromone in this Location."""
		self.pheromone -= self.pheromone * (1.0 / 30)
	

class World:
	"""Class that represents the entire world the Ants live in.
	Contains Locations and Ants, and is meant to be instantiated once.
	"""
	
	MAX_ANTS = 20
	
	def __init__(self):
		self.ants = {}
		self.locations = {}
		self.p_food = 0
	
	def place_food(self, p):
		"""Place food in all Locations with probability p."""
		self.p_food = p
		for point in self.locations:
			point.place_food(p)
	
	def remove_food(self, pos):
		"""Remove one unit of food from the Location at pos."""
		self.locations[pos].remove_food();
	
	def has_food(self, pos):
		"""Returns true if the Location at pos has at least one unit
		of food, false otherwise.
		"""
		return self.get_location(pos).has_food();
		
	def add_ant(self):
		"""Add an Ant to the nest."""
		ant = Ant(self)
		pos = ant.getPos()
		if pos in self.ants:
			self.ants[pos].append(ant)
		else:
			self.ants[pos] = [ant]
	
	def add_ants(self, n):
		"""Add n ants to the nest."""
		for i in xrange(n):
			self.add_ant()
	
	def __repr__(self):
		"""Return a string representation of this World."""
		return str(self.ants)
	
	def move_ants(self):
		"""Iterate through and move all the Ants in the World."""
		ants = []
		for pos, antlist in self.ants.iteritems():
			for ant in antlist:
				ant.move()
				ants.append(ant)
		self.evaporate_pheromone()
		d = {}
		for ant in ants:
			pos = ant.getPos()
			if pos in d:
				d[pos].append(ant)
			else:
				d[pos] = [ant]
		self.ants = d
	
	def get_location(self, pos):
		"""Returns the Location at pos, creating it if it doesn't 
		already exist.
		"""
		if pos not in self.locations:
			loc = Location()
			self.locations[pos] = loc
			if self.p_food > 0:
				loc.place_food(self.p_food)
		else: 
			loc = self.locations[pos]
		return loc
	
	def add_pheromone(self, pos, amount=1):
		"""Adds amount pheromone to the Location at pos."""
		self.get_location(pos).add_pheromone(amount)
	
	def get_pheromone(self, pos):
		"""Returns the amount of pheromone in the Location at pos."""
		return self.get_location(pos).get_pheromone();
	
	def set_pheromone(self, pos, amount):
		"""Sets the amount of pheromone in the Location at pos to
		amount.
		"""
		self.get_location(pos).set_pheromone(amount)
	
	def evaporate_pheromone(self):
		"""Evaporates pheromone from all existing Locations."""
		for pos, loc in self.locations.iteritems():
			loc.evaporate_pheromone()
	
	def get_ant_dict(self):
		"""Returns a representation of all the Ants in the World.
		The return value is a dictionary of the form
		{(x, y):number_of_ants} with one (x, y) key for each
		Location that contains at least one Ant.
		"""
		return self.ants
	
	def num_ants(self, pos):
		"""Returns the number of Ants at pos."""
		if pos in self.ants:
			return len(self.ants[pos])
		else: return 0

	def at_capacity(self, pos):
		"""Returns True if the Location at pos is full with Ants,
		False otherwise.
		"""
		return self.num_ants(pos) >= World.MAX_ANTS

class AntPlot:
	"""Class that uses wx to draw a plot of the Ants in the World."""
	
	def __init__(self, world):
		self.world = world
		self.app = wx.PySimpleApp()
		self.w = 500
		self.h = 500
		self.frame = wx.Frame(None, -1, 'Ant Plot', 
				      size=(self.w, self.h))
		self.canvas = FloatCanvas(self.frame, -1)
		
	
	def draw(self):
		"""Pops up a wx window that represents the current state of
		the World.
		"""
		positions = self.world.get_ant_dict()
		for pos in positions:
			x, y = pos
			x -= self.w / 2
			y -= self.h / 2
			self.canvas.AddPoint((x, y))
		self.frame.Show()
		self.app.MainLoop()
		
if __name__ == "__main__":
	world = World()
	world.place_food(0.5)
	try:
		timesteps = int(sys.argv[1])
	except:
		sys.stderr.write("Usage: python ants.py [timesteps]\n")
		sys.exit(1)
	for i in range(timesteps):
		world.add_ants(10)
		world.move_ants()
	plot = AntPlot(world)
	plot.draw()

