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

from uuid import uuid4

class Location:
  def __init__(self,name = "Location",symbol = "!",start_location = False):
    self.name = name
    self.id = uuid4()
    self.symbol = symbol
    self.jobs = []
    self.courses = []
    self.items = []
    self.start_location = start_location
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def __repr__(self):
    return str(self.symbol)
  
  def debug_string(self):
    """For debugging, print out all of the variables of this object"""
    s = "Name:\t%s" % self.name
    s += "\nID:\t%s" % self.id
    s += "\nSymbol:\t%s" % self.symbol
    s += "\nJobs: %s" % str(self.jobs)
    s += "\nCourses: %s" % str(self.courses)
    s += "\nItems: %s" % str(self.items)
    return s
  
  def add_job(self,new_job):
    """Add the Job object to the list of jobs if it doesn't already exist.'"""
    
    if new_job not in self.jobs:
      self.jobs.append(new_job)
      return True
    return False
  
  def add_course(self, new_course):
    """Add the Course object to the list of available courses if it doesn't already exist."""
    if new_course not in self.courses:
      self.courses.append(new_course)
      return True
    return False
  
  def get_job_by_symbol(self,symbol):
    for job in self.jobs:
      if symbol == job.symbol:
        return job
    return None
  
  def get_job_by_rank(self,rank):
    for job in self.jobs:
      if int(rank) == job.rank:
        return job
    return None
  
  def get_course_by_number(self,symbol):
    for course in self.courses:
      if int(symbol) == course.symbol:
        return course
    return None
  
  def add_item(self,new_item):
    """Add the item to the list if it doesn't already exist"""
    if new_item not in self.items:
      self.items.append(new_item)
      return True
    return False
  
  def get_item(self,id = None,delete = False):
    """Return an item referenced by any key, such as ID or name.
    
    If delete is True, then the item will be removed from the items list."""
    
    i = 0
    if id:
      for item in self.items:
        if item.id is id:
          return self.items.pop(i) if delete else item
        i += 1
  
  def has_items(self):
    return True if self.items and len(self.items) > 0 else False
