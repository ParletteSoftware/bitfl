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
from menu import NewGameMenu
from menu import TurnMenu
from player import Player
from map import Map

class Game:
  def __init__(self):
    self.id = uuid4()
    #Valid commands this game class will accept
    self.commands = ["move","end"]
    #Has the game been started?
    self.started = False
    #List of player objects
    self.players = list()
    #Game Board
    self.map = Map()
    #Turn Counter
    self.turn = 0
  
  def start(self):
    menu = NewGameMenu()
    
    #Display the menu until the user quits or starts the game
    while True:
      selection = menu.display().lower()
      if selection == 'q':
        break
      if selection == 's':
        self.new_turn()
        self.started = True
        break
      if selection == 'a':
        name = raw_input("Name: ")
        if name is not "":
          self.players.append(Player(name))
      if selection == 'l':
        print "Player List:"
        print "\n".join(str(x) for x in self.players)
    
    return self.started
  
  def run(self):
    """Process user commands until they want to exit."""
    #Loop until something breaks it, like a quit event
    menu = TurnMenu()
    while True:
      for player in self.players:
        turn_done = False
        while not turn_done:
          selection = menu.display(self.turn,player.name)
          if selection == 'q':
            return True
          if selection == 'e':
            turn_done = True
          if selection == 'm':
            print "Map:\n%s" % (self.map)
            self.command("move",{'player':player,'location':''})
      self.new_turn()
  
  def new_turn(self):
    """Create a new turn and add it to the end of the turns list."""
    if self.turn > 0:
      #End the current turn
      pass
    
    #Advance the turn counter
    self.turn += 1
  
  def command(self,command,parameters = None):
    """Process a command for a player.
    
    Return a boolean on if the command completed successfully."""
    
    # Parameters need to be provided
    if command is None:
      return False
    
    # Parameters need to be valid
    if command not in self.commands:
      return False
    
    if command is "move":
      #Move Player
      #Verify Parameters
      if parameters:
        if set(['player','location']).issubset(parameters):
          pass
        else:
          print "invalid parameters for move command"
      return False
    
    if command is "end":
      #End Turn
      return True
    
    #If we got here, then something didn't execute correctly
    return False
