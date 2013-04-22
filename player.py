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
    self.knowledge = 0
    self.completed_education = []
    self.money = 0
    self.items = []
    self.attributes = {'hunger': 0,
                       'fatness': 0,
                      }
  
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
    
    s = "%s\n%s\nLocation:\t%s\n" % (self.name,"=" * len(self.name),self.location.name)
    if self.job:
      s += "Job:\t\t%s at %s ($%s pay per unit)\n" % (str(self.job),str(self.job.location.name),str(self.job.pay))
    else:
      s += "Job:\t\tNone\n"
    s += "Current money:\t$%s\n" % (str(self.money))
    s += "Knowledge:\t%s\nClasses:\n\t%s\n" % (str(self.knowledge),"\n\t".join(self.completed_education) if self.completed_education else "None")
    
    s += "Items:\n\t%s\n" % ("\n\t".join(str(x) for x in self.items) if self.items else "None")
    s += "Happiness:\t%s\n" % (str(self.happiness()))
    for attribute,value in self.attributes.iteritems():
      s += "%s:\t%s\n" % (str(attribute).capitalize(),str(value))
    return s
  
  def happiness(self):
    """Return a happiness value that is calculated from the player's attributes"""
    happiness = self.knowledge / 10
    happiness += self.money / 100
    happiness += len(self.completed_education)
    if self.job:
      happiness += self.job.rank
    
    return happiness

  def add_item(self,new_item):
    if new_item:
      self.items.append(new_item)
  
  def use_item(self,item):
    """Consume the item, applying its effects on this player instance."""
    if item in self.items:
      for effect in item.effects:
        if effect in self.attributes:
          self.attributes[effect] += item.effects[effect]
          #Set the value to 0 if it just went below 0
          if self.attributes[effect] < 0:
            self.attributes[effect] = 0
      self.items.remove(item)
