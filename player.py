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

class Player:
  def __init__(self,name = "Player"):
    self.name = name
    self.id = uuid4()
    self.location = None
    self.job = None
    self.turns = 0
  
  def __repr__(self):
    return str(self.name)
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def move(self,new_location):
    """Change the player's location variable.
    The validity of this move should be done before this function is called."""
    self.location = new_location
    return True

  def info_display(self):
    """Return a string with an information display for this player"""
    
    return "%s\n%s\nLocation:\t%s\nJob:\t\t%s\n" % (self.name,"=" * len(self.name),self.location.name,str(self.job))
