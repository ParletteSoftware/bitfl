"""Billy in the Fat Lane - A Lame Life Simulation Game
Copyright (C) 2013 Chris Parlette, Matt Parlette

This file is part of Billy in the Fat Lane.

Billy in the Fat Lane is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Billy in the Fat Lane is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Billy in the Fat Lane.  If not, see http://www.gnu.org/licenses/."""

from numpy import *
from location import Location
from json import load
import os

class Map:
  def __init__(self, map_path = None, debug = False):
    self.debug = debug
    self.log_debug("map_path received as %s" % str(map_path))
    if map_path and os.path.exists(map_path):
      
      #Load from map_path if it is provided
      self.load_from_file(map_path)
    else:
      #File is inavlid, create a generic game board for debug
      self.grid = empty((10,10),dtype='object') #This initializes all points to None
      self.title = "map"
  
  def __repr__(self):
    return str(self.grid)
  
  def log_debug(self,message):
    if self.debug:
      print "Map Class:\tDebug:\t%s" % str(message)
  
  def log_error(self,message):
    print "Map Class:\tError:\t%s" % str(message)
  
  def load_from_file(self,map_path):
    conf_file = os.path.join(map_path,"map.json")
    
    #Open the file for reading
    f = open(conf_file,'r')
    print str(f)
    
    if f:
      self.log_debug("File (%s) Opened" % (conf_file))
      
      #Read in the entire file and load it as json
      map_conf = load(f)
      self.log_debug("Loaded JSON from file")
      self.log_debug("JSON: %s" % str(map_conf))
      
      #Set the map settings
      #try:
      self.title = map_conf["general"]["title"]
      
      #Close the file
      f.close()
    else:
      self.log_error("File (%s) could not be opened" % (conf_file))
  
  def add(self,x,y,location):
    """Add a location to a point on the map."""
    pass
