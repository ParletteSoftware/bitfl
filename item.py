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

class Item:
  def __init__(self,name = "Unnamed Item",
               symbol = "!",
               availability = 50,
               cost = 1,
               effects = {}):
    self.name = name
    self.id = uuid4()
    #Symbol: the command for a user to reference this item
    self.symbol = symbol
    #Availability: The rarity of this item
    #(100 is common, 1 is very rare)
    self.availability = availability
    #Cost: The cost to buy this item
    self.cost = cost
    
    #Effects: What will this item do?
    self.effects = effects
  
  def __repr__(self):
    return str(self.name)
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def __gt__(self,other):
    return self.name > other.name if hasattr(other,"name") else False
