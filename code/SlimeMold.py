"""
This module contains the necessary classes for the Slime-Mold implementation.

The implementation was elaborated during the Olin College's Computational Modeling 
class of Allen Downey (fall 2011) by Teodora Vidolova and Charles Szersnovicz and is part
of the corresponding case-study.

"""

from src import CellWorld, World, Animal           # Copyright A.Downey
import random, Tkinter, numpy

class MoldWorld(CellWorld):
    """Provides a grid of patch that contained a density of pheromone and can be occupied by a mold"""
    
    def __init__(self, canvas_size = 600, patch_size = 5):
        CellWorld.__init__(self, canvas_size, patch_size)
        self.title("MoldWorld")
        self.canvas_size = canvas_size
        self.patch_size = patch_size
        self.setupGUI()
        self.setup()
    
    def setupGUI(self):
        """Makes the GUI, the environment"""
        
        self.counter = 0
        self.row()
        self.make_canvas()
        
        # right frame and buttons
        self.col([0])
        self.bu(text='Make Mold', command=self.make_mold)
        self.bu(text='Run', command=self.run)
        self.bu(text='Stop', command=self.stop)
        self.bu(text='Step', command=self.step)
        self.bu(text='Clear', command=self.clear)
        self.bu(text='Restart', command=self.setup)
        self.bu(text='Quit', command=self.quit)
        self.label = self.la(text='Step: ' + str(self.counter))
        self.slider_evap = Tkinter.Scale(self, from_=0, to=1, resolution=0.01, 
                               orient="horizontal", label="Evaporation:", command=self.update_values)
        self.slider_diff = Tkinter.Scale(self, from_=0, to=1, resolution=0.01, 
                               orient="horizontal", label="Diffusion:", command=self.update_values)
        self.slider_evap.set(.95)
        self.slider_diff.set(.95)
        self.slider_evap.pack(side="left")
        self.slider_diff.pack()
        self.endcol()
    
    def setup(self):
        """Makes the environment"""
        
        self.counter = 0
        #putting the patches
        self.grid = {}
        pattern = int(0.5*self.canvas_size/self.patch_size) 
        y = -pattern
        while y < pattern:
            x = -pattern
            while x < pattern:
                self.grid[x,y] = Patch(self, x, y)
                x += 1
            y += 1
#        self.grid[0,0].density = 100
        self.clear()

    def get_patch(self, x, y):
        """Returns the patch with x, y indices"""
        try:
            return self.grid[x,y]
        except:
            return 'Exception'
        
    def make_mold(self):
        """Makes a Mold with a random position"""
        
        boundary = 0.5*self.canvas_size/self.patch_size
        for i in range(1000):
#            mold = Mold(self, random.randint(-boundary+20, boundary-20), random.randint(-boundary+20, boundary-20))
            mold = Mold(self, random.randint(-boundary, boundary-1), random.randint(-boundary, boundary-1))
#        mold = Mold(self, random.randint(-boundary, boundary-1), random.randint(-boundary, boundary-1))
#        return mold
    
    def step(self):
        """Executes an iteration"""

        for animal in self.animals:
            animal.step()
                
        for key in self.grid:
            self.grid[key].step()
        
        self.count()
    
    def count(self):
        """Updates the iteration counter"""
        
        self.counter += 1
        self.label.config(text='Step: ' + str(self.counter))
               
    def clear(self):
        """Cleans all Molds and resets all patches"""
        
        for animal in self.animals:
            animal.undraw()
        self.animals = []
        
        for key in self.grid:
            self.grid[key].occupied = False
    
    def update_values(self, event):
        """Set the new coefficients of diffusion and evaporation from the sliders"""
        
        for key in self.grid:
            self.grid[key].evap_coef = self.slider_evap.get()
            self.grid[key].diff_coef = self.slider_diff.get()
                

class Patch(object):
    """This class implements a slime-mold world Patch, component of the grid
    Attributes:
        world, x, y, density 
    """
    
    def __init__(self, world, x, y, density = 0):
        self.world = world
        self.density = density
        self.set_color()
        self.x = x
        self.y = y
        self.occupied = False
        self.bounds = self.world.cell_bounds(self.x, self.y)
        self.item = self.world.canvas.rectangle(self.bounds[::2], fill = self.color)
        self.evap_coef = 0
        self.diff_coef = 0
    
    def step(self):
        """Executes the instructions included in one step or iteration"""
        
        self.diffuse()
        self.evaporate()
        self.set_color()
        self.actualize()
        
    def set_color(self):
        """Sets self.color"""
        
        self.color = 'grey' + str(100 - self.density)
            
    def actualize(self):
        """Updates the patch"""
        
        self.item.config(fill = self.color)

    def evaporate(self):
        """Decreases the density at each step"""
        
        if self.occupied is False:
            if self.density > 0:
                self.density = int(self.evap_coef*self.density)
            else:
                self.density = 0
            
    def receive(self):
        """Increases by one the density"""
        
        if self.density < 100:
            self.density += 1
        else:
            self.density = 100

    def diffuse(self):
        """Applies the diffusion mechanism"""
        
        valid_neighbors = []
        neighbors = self.get_neighbors()
        for neighbor in neighbors:
            if neighbor != 'Exception':
                valid_neighbors.append(neighbor.density)
        maxDensity = max(valid_neighbors)
        if self.density < maxDensity:
            self.density = int(self.diff_coef*maxDensity)
    
    def get_neighbors(self):
        """Returns a list of the eight patch neighbors"""
        
        x = self.x
        y = self.y
        return [self.world.get_patch(x-1, y+1), self.world.get_patch(x, y+1), self.world.get_patch(x+1, y+1), self.world.get_patch(x-1, y), 
            self.world.get_patch(x+1, y), self.world.get_patch(x-1, y-1), self.world.get_patch(x, y-1), self.world.get_patch(x+1, y-1)]


class Mold(Animal):
    """This class implements a slime-mold Mold
    
    Attributes:
        dir: direction, one of [0, 1, 2, 3]
    """
    
    aheads_orthos = {0:[numpy.array([1,0]), numpy.array([0,1])], 1:[numpy.array([0,1]), numpy.array([1,0])],
                 2:[numpy.array([-1,0]), numpy.array([0,-1])], 3:[numpy.array([0,-1]), numpy.array([-1,0])]}
    
    def __init__(self, world, x, y, dir=random.randint(0,3)):
        Animal.__init__(self, world, x, y)
        self.draw()
        self.dir = dir
        self.x = x
        self.y = y
    
    def draw(self):
        """Draw the mold"""
        
        #bounds of the patch
        bounds = self.world.cell_bounds(self.x, self.y)
        #draw a square
        self.tag = self.world.canvas.polygon(bounds, fill = 'brown')
        
    def emit(self):
        """Emits a pheromone dose"""
        self.world.get_patch(self.x, self.y).receive()
        
    def sniff(self):
        """Mold looks at the three patches ahead and 
           goes on the one which has the max density
        """
        
        patches_ahead = []
        patch = numpy.array([self.x, self.y])
        
        for i in range(-1, 2):
            patch_ahead = patch + Mold.aheads_orthos[self.dir][0] + i*Mold.aheads_orthos[self.dir][1]
            patch_ahead = self.world.get_patch(patch_ahead[0], patch_ahead[1])
            if patch_ahead != 'Exception' and patch_ahead.occupied is False:
                patches_ahead.append((patch_ahead.density, patch_ahead))
        self.dir = random.choice([0,1,2,3])
        
        if patches_ahead != []:
            valid_patches = []
            # tuple (maxDensity, maxPatch) 
            patches_ahead.sort(reverse=True)
            for density, patch in patches_ahead:
                if density == patches_ahead[0][0]:
                    valid_patches.append(patch)
            
            #move the mold to that patch or one of them
            self.move(valid_patches[random.randint(0,len(valid_patches)-1)])
    
    def move(self, patch):
        """Move the mold to the patch"""
        
        self.world.get_patch(self.x, self.y).occupied = False
        patch.occupied = True
        self.x = patch.x
        self.y = patch.y
        self.redraw()
                                          
    def step(self):
        """Implements the rule of Reisnick's mold"""
        
        self.emit()
        self.sniff()
        

if __name__ == '__main__':
    world = MoldWorld()
    world.mainloop()
