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

class Job:
  def __init__(self,name = "Unnamed Job",
               symbol = "!",
               availability = 50,
               pay = 1,
               rank = 0,
               location = None):
    self.name = name
    self.id = uuid4()
    #Symbol: the command for a user to reference this job
    self.symbol = symbol
    #Availability: The percentage of openings for this job
    #(100 is always available, 0 is never available)
    self.availability = availability
    #Pay: Pay per unit of time
    self.pay = pay
    #Rank: Where this job stands with regard to other jobs at its location
    self.rank = rank
    #Location: The location of this job
    self.location = location
  
  def __repr__(self):
    return str(self.name)
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def __gt__(self,other):
    return self.rank > other.rank if hasattr(other,"rank") else False
  
  def __lt__(self,other):
    return self.rank < other.rank if hasattr(other,"rank") else False
  
