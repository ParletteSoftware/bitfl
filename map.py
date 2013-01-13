from numpy import *

class Map:
  def __init__(self, x = 10, y = 10):
    #Create the grid
    self.grid = empty((x,y),dtype='object') #object may be something more specific later
  
  def __repr__(self):
    return str(self.grid)
