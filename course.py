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

class Course:
  def __init__(self,name = "Unnamed Course",
               symbol = 12345,
               knowledge_value = 50,
               time = 50,
               knowledge_required = 0
               class_required = None
               cost = 98765):
    self.name = name
    self.id = uuid4()
    #Symbol: the command for a user to reference this course
    self.symbol = symbol
    #Knowledge Value: How much the players knowledge increases from this course
    self.knowledge_value = knowledge_value
    #Time: Amount of time the course takes
    self.time = time
    #Knowledge Required: Base amount of knowledge required to take this course
    self.knowledge_required = knowledge_required
    #Class Required: An optional prerequisite course
    self.class_required = class_required
    #Cost: Amount of money it takes to enroll in this course
    self.cost = cost
  
  def __repr__(self):
    return str(self.name)
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def __gt__(self,other):
    return self.rank > other.rank if hasattr(other,"rank") else False
  
  def __lt__(self,other):
    return self.rank < ot