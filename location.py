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
  def __init__(self,name = "Location",symbol = "!"):
    self.name = name
    self.id = uuid4()
    self.symbol = symbol
    self.jobs = []
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def __repr__(self):
    return str(self.symbol)
  
  def add_job(self,new_job):
    """Add the Job object to the list of jobs if it doesn't already exist.'"""
    
    if new_job not in self.jobs:
      self.jobs.append(new_job)
      return True
    return False
  
  def get_job_by_symbol(self,symbol):
    for job in self.jobs:
      if symbol == job.symbol:
        return job
    return None
