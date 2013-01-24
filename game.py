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
from menu import NewGameMenu,TurnMenu, MoveMenu
from player import Player
from map import Map

class Game:
  def __init__(self, map = None, debug = False):
    self.id = uuid4()
    self.debug = debug
    #Valid commands this game class will accept
    self.commands = ["move","end"]
    #Has the game been started?
    self.started = False
    #List of player objects
    self.players = list()
    #Game Board
    self.map = map if map else Map()
    #Turn Counter
    self.turn = 0
  
  def log_debug(self,message):
    if self.debug:
      print "Game Class:\tDebug:\t%s" % str(message)
  
  def log_error(self,message):
    print "Game Class:\tError:\t%s" % str(message)
  
  def get_location(self,symbol):
    if symbol and isinstance(symbol,basestring):
      for location in self.map.locations:
        if symbol == location.symbol:
          return location
    return None
  
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
          player = Player(name)
          self.players.append(player)
          
          #Set the player with a location to start
          player.move(self.map.locations[0])
      if selection == 'l':
        print "Player List:"
        print "\n".join(str(x) for x in self.players)
    
    return self.started
  
  def run(self):
    """Process user commands until they want to exit."""
    #Loop until something breaks it, like a quit event
    menu = TurnMenu()
    move_menu = MoveMenu(self.map.locations)
    while True:
      for player in self.players:
        turn_done = False
        while not turn_done:
          selection = menu.display(self.turn,player)
          if selection == 'q':
            return True
          if selection == 'e':
            turn_done = True
          if selection == 'm':
            self.command("move",{'player':player,'location_symbol':move_menu.display(self.map)})
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
    
    self.log_debug("command(): command is %s" % str(command))
    self.log_debug("command(): parameters: %s" % str(parameters))
    
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
        if set(['player','location_symbol']).issubset(parameters):
          #User may have cancelled on MoveMenu, so make sure a location was passed
          if parameters['location_symbol'] != "":
            location = self.get_location(parameters['location_symbol'])
            self.log_debug("Moving %s to %s" % (parameters['player'],location.name))
            parameters['player'].move(location)
        else:
          self.log_error("Invalid parameters for move command")
      return False
    
    if command is "end":
      #End Turn
      return True
    
    #If we got here, then something didn't execute correctly
    return False
