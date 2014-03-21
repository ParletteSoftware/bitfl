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
from job import Job
from json import load
from course import Course
from item import Item
import os

class Map:
  def __init__(self, map_path = None, debug = False):
    self.debug = debug
    self.log_debug("map_path received as %s" % str(map_path))
    
    #Initialize the lists
    self.locations = []
    
    if map_path and os.path.exists(map_path):
      
      #Load from map_path if it is provided
      self.load_from_file(map_path)
      self.log_debug("map generated:\n%s" % str(self))
    else:
      #File is inavlid, create a generic game board for debug
      self.grid = empty((10,10),dtype='object') #This initializes all points to None
      self.title = "map"
  
  def __repr__(self):
    s = ""
    for row in self.grid:
      for point in row:
        s += " %s " % str(point) if point else " - "
      s += "\n"
    s += "\n%s" % ("\n".join("\t%s: %s" % (x.symbol,x.name) for x in self.locations))
    return s
  
  def log_debug(self,message):
    if self.debug:
      print "Map Class:\tDebug:\t%s" % str(message)
  
  def log_error(self,message):
    print "Map Class:\tError:\t%s" % str(message)
  
  def load_from_file(self,map_path):
    conf_file = os.path.join(map_path,"map.json")
    
    #Open the file for reading
    f = open(conf_file,'r')
    
    if f:
      self.log_debug("File (%s) Opened" % (conf_file))
      
      #Read in the entire file and load it as json
      map_conf = load(f)
      self.log_debug("Loaded JSON from file")
      self.log_debug("JSON: %s" % str(map_conf))
      
      #Set the map settings
      try:
        self.title = map_conf["general"]["title"]
        self.x_size = map_conf["general"]["x_size"]
        self.y_size = map_conf["general"]["y_size"]
      except KeyError,e:
        self.log_error("Invalid config file: %s is missing" % str(e))
        return
      
      #Now setup the game board
      self.generate_grid(self.x_size,self.y_size)
      
      #Add locations to the grid
      for location_json in map_conf["locations"]:
        if "start_location" in location_json and location_json["start_location"]:
          start_location = True
        else:
          start_location = False
        self.log_debug("Processing location JSON %s" % str(location_json))
        location = Location(name=location_json["title"],symbol=location_json["symbol"],start_location=start_location)
        
        #Parse the jobs for this location
        if "jobs" in location_json:
          for job_json in location_json["jobs"]:
            self.log_debug("Processing job JSON %s" % str(job_json))
            job = Job(name=job_json["title"],
                      symbol=job_json["symbol"] if "symbol" in job_json else "",
                      availability=job_json["availability"],
                      pay=job_json["pay"],
                      rank=job_json["rank"],
                      location=location)
            location.add_job(job)
        if "education" in location_json:
          for class_json in location_json["education"]:
            self.log_debug("Processing class JSON %s" % str(class_json))
            course = Course(name=class_json["title"],
                            symbol=class_json["symbol"],
                            knowledge_value=class_json["knowledge_value"],
                            time=class_json["time"],
                            knowledge_required=class_json["knowledge_required"],
                            course_required=class_json["course_required"] if "course_required" in class_json else None,
                            cost=class_json["cost"])
            location.add_course(course)
        if "items" in location_json:
          for items_json in location_json["items"]:
            self.log_debug("Processing item JSON %s" % str(items_json))
            effects = {}
            if "effects" in items_json:
              for effect in items_json["effects"]:
                self.log_debug("Processing effect json: %s" % str(effect))
                effects[effect['attribute']] = effect['value']
            self.log_debug("Loaded effects as %s" % (str(effects)))
            item = Item(name=items_json["title"],
                      symbol=items_json["symbol"] if "symbol" in items_json else "",
                      availability=items_json["availability"],
                      cost=items_json["cost"],
                      effects=effects,
                      consumable=items_json["consumable"] if "consumable" in items_json else True,
                      )
            location.add_item(item)
            self.log_debug("Added item:\n%s" % item.debug_string())
        
        #Finally add this location to the map
        self.log_debug("Loaded location from file:\n%s" % location.debug_string())
        self.add_location(location_json["x"],location_json["y"],location)
      
      #Close the file
      f.close()
    else:
      self.log_error("File (%s) could not be opened" % (conf_file))
  
  def generate_grid(self,x,y):
    """Generate a map grid with the given x and y parameters."""
    
    self.grid = empty((int(x),int(y)),dtype='object') #This initializes all points to None
  
  def add_location(self,x,y,location):
    """Add a location to a point on the map."""
    
    #Check to make sure we aren't reusing symbols
    symbolExists = False
    for loc in self.locations:
      if loc.symbol == location.symbol:
        symbolExists = True
    
    if symbolExists:
      self.log_error("The symbol (%s) is already used, so I cannot add %s" % (location.symbol,location.name))
    elif self.grid[x][y] is None:
      #Add the location to the point on the grid
      self.grid[x][y] = location
      #Also keep a list of locations for easier access
      self.locations.append(location)
    else:
      self.log_error("There was already something (%s) at map location (%s,%s), so I cannot add %s" % (self.grid[x][y].name,str(x),str(y),location.name))
  
  def get_start_location(self):
    """Return the location marked as start_location."""
    for location in self.locations:
      if location.start_location:
        return location
    return None
