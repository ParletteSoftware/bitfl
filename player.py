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
    self.attributes = {"health": Health(10),
                       "knowledge": Knowledge(),
                       "happiness": Happiness(),
                       "money": Money(),
                       "time": Time()}
  
  def __repr__(self):
    return str(self.value)
  
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
    s += "Current money:\t$%s\n" % (str(self.attributes['money'].get()))
    s += "Knowledge:\t%s\nClasses:\n\t%s\n" % (str(self.attributes['knowledge'].get()),"\n\t".join(self.completed_education) if self.completed_education else "None")
    
    s += "Items:\n\t%s\n" % ("\n\t".join(str(x) for x in self.items) if self.items else "None")
    s += "Happiness:\t%s\n" % (str(self.attributes['happiness'].get()))
    return s
  
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
      for attribute in item.effects:
        if attribute in self.attributes:
          self.attributes[attribute].set(delta=item.effects[attribute])
      self.items.remove(item)

class Attribute(object):
  def __init__(self,name="Attribute",value=0):
    self.name = name
    self.id = uuid4()
    self.value = value
    self.minor_attributes = None
  
  def __repr__(self):
    return str(self.name)
  
  def set(self,value = 0, delta = 0):
    """Change the value of this attribute.
    If value is provided, then the attriute value is set to this number.
    Otherwise, if delta is provided, the attribute value will add this to its current value.
    If neither is provided, then this method does nothing."""
    
    if value:
      self.value = value
    elif delta:
      self.value += delta
    else:
      return
  
  def get(self):
    """Return the calculated value for this attribute."""
    self.calculate()
    return self.value
  
  def calculate(self):
    """Override this method to define how this attribute's value is calculated.'"""
    pass
  
class Happiness(Attribute):
  def __init__(self,value=0):
    super(Happiness,self).__init__("Happiness",value)
    #Attribute.__init__(self,"Happiness",value)
  
  def calculate(self):
    pass

class Health(Attribute):
  def __init__(self,value=0):
    super(Health,self).__init__("Health",value)
    #Attribute.__init__(self,"Health",value)
  
  def calculate(self):
    pass

class Knowledge(Attribute):
  def __init__(self,value=0):
    super(Knowledge,self).__init__("Knowledge",value)
    #Attribute.__init__(self,"Knowledge",value)
  
  def calculate(self):
    pass
  
class Money(Attribute):
  def __init__(self,value=0):
    super(Money,self).__init__("Money",value)
    #Attribute.__init__(self,"Money",value)
  
  def calculate(self):
    pass

class Time(Attribute):
  def __init__(self,value=0):
    super(Time,self).__init__("Time",value)
  
  def calculate(self):
    pass
