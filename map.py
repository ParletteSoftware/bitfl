from numpy import *
from location import Location

class Map:
  def __init__(self, x = 10, y = 10):
    #Create the grid
    self.grid = empty((x,y),dtype='object') #This initializes all points to None
  
  def __repr__(self):
    return str(self.grid)
  
  def add(self,x,y,location):
    """Add a location to a point on the map."""
    pass
