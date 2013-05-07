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
    self.completed_education = []
    self.items = []
    #Major Attributes
    self.health = Health()
    self.knowledge = Knowledge()
    self.happiness = Happiness()
    self.money = 0
  
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
    s += "Knowledge:\t%s\nClasses:\n\t%s\n" % (str(self.knowledge.get()),"\n\t".join(self.completed_education) if self.completed_education else "None")
    
    s += "Items:\n\t%s\n" % ("\n\t".join(str(x) for x in self.items) if self.items else "None")
    s += "Happiness:\t%s\n" % (str(self.happiness.get()))
  
  def get_happiness(self):
    """Set the happiness instance variable calculated by the player's attributes and return it.
    
    WARNING: This method is deprecated. Use Player.happiness.get() instead."""
    return self.happiness.get()

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

class Attribute:
  def __init__(self,name="Attribute",value=0):
    self.name = name
    self.id = uuid4()
    self.value = value
    self.minor_attributes = None
  
  def __repr__(self):
    return str(self.name)
  
  def get():
    """Return the calculated value for this attribute."""
    self.calculate()
    return self.value
  
  def calculate(self):
    """Override this method to define how this attribute's value is calculated.'"""
    pass
  
class Happiness(Attribute):
  def __init__(self,value=0):
    super(Happiness,self).__init__("Happiness",value)
  
  #TODO: how can I pass these values in without explicitly passing them?
  def calculate(self):
    pass

class Health(Attribute):
  def __init__(self,value=0):
    super(Health,self).__init__("Health",value)
  
  def calculate(self):
    pass

class Knowledge(Attribute):
  def __init__(self,value=0):
    super(Knowledge,self).__init__("Knowledge",value)
  
  def calculate(self):
    pass
  
