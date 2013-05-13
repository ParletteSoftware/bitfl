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
from menu import NewGameMenu,TurnMenu, MoveMenu, JobMenu, CourseMenu, BuyMenu, ListMenu
from player import Player
from map import Map
import os

class Game:
  def __init__(self, map = None, debug = False):
    self.id = uuid4()
    self.debug = debug
    #Valid commands this game class will accept
    self.commands = ["move","end","job_apply", "job_work", "course_enroll",
                     "item_buy","item_use"]
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
      """Clear the screen, use cls if Windows or clear if Linux"""
      if not self.debug:
        os.system('cls' if os.name=='nt' else 'clear')
      if selection == 'q':
        break
      if selection == 's':
        if not self.players:
          print "No players added, please add a player before starting the game."
        else:
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
    move_menu = MoveMenu(self.map.locations)
    while True:
      for player in self.players:
        turn_done = False
        while not turn_done:
          menu = TurnMenu()
          if player.location.jobs:
            menu.add_option('a','Apply for a job')
          if player.job in player.location.jobs:
            menu.add_option('w','Work')
          if player.location.courses:
            menu.add_option('c','Enroll in a course')
          if player.location.has_items():
            menu.add_option('b','Buy Items')
          if len(player.items):
            menu.add_option('u','Use Item')
            
          selection = menu.display(self.turn,player,player.attributes['time'].get())
          
          """Clear the screen, use cls if Windows or clear if Linux"""
          if not self.debug:
            os.system('cls' if os.name=='nt' else 'clear')
          if selection == 'q':
            return True
          if selection == 'e':
            player.attributes['time'].set(value=10)
            turn_done = True
          if selection == 'm':
            self.command("move",{'player':player,'location_symbol':move_menu.display(self.map)})
          if selection == 'a':
            self.command('job_apply',{'player':player, 'job_rank':JobMenu().display(job_list=player.location.jobs)})
          if selection == 'w':
            self.command('job_work',{'player':player})
          if selection == 'i':
            print player.info_display()
          if selection == 'c':
            self.command('course_enroll',{'player':player, 'course_choice':CourseMenu().display(course_list=player.location.courses, player=player)})
          if selection == 'b':
            item = BuyMenu().display(player.location.items)
            if item:
              self.command('item_buy',{'player':player, 'item':item})
          if selection == 'u':
            item = ListMenu("Select Item to Use",player.items).display()
            self.command('item_use',{'player':player, 'item':item})
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
      self.log_debug("command(): command was None")
      return False
    
    # Parameters need to be valid
    if command not in self.commands:
      self.log_debug("command(): command was not in self.commands")
      return False
    
    if command is "move":
      #Move Player
      #We're going to start with each movement costing 1 hour, this will likely change
      time_cost = -1
      #Verify Parameters
      if parameters:
        if set(['player','location_symbol']).issubset(parameters):
          #Check to see if they have enough time to move
          if parameters['player'].attributes['time'].get() >= abs(time_cost):
            #User may have cancelled on MoveMenu, so make sure a location was passed
            if parameters['location_symbol'] != "":
              location = self.get_location(parameters['location_symbol'])
              self.log_debug("Moving %s to %s" % (parameters['player'],location.name))
              parameters['player'].move(location)
              parameters['player'].attributes['time'].set(delta=time_cost)
          else:
            print "No time is left to move!"
        else:
          self.log_error("Invalid parameters for move command")
      else:
        self.log_error("Inavlid parameters for apply command")
      return False
    
    if command is "job_apply":
      #Apply for a job
      #Each job application will cost 1 hour to start
      time_cost = -1
      #Verify Parameters
      if parameters:
        if set(['player','job_rank']).issubset(parameters):
          player = parameters['player']
          #Check to see if they have enough time to apply for this job
          if player.attributes['time'].get() >= abs(time_cost):
            if parameters['job_rank'] != '':
              self.log_debug("Looking up job (rank %s) in %s" % (parameters['job_rank'],player.location.name))
              job = player.location.get_job_by_rank(parameters['job_rank'])
              if job:
                self.log_debug("Player %s applying for %s at %s" % (player,job.name,player.location.name))
                player.job = job
                player.attributes['time'].set(delta=time_cost)
              else:
                self.log_error("Job (rank %s) not found in %s" % (parameters['job_rank'],player.location.name))
          else:
            print "No time is left to apply for this job!"
        else:
          self.log_error("Inavlid parameters for apply command")  
      else:
        self.log_error("Inavlid parameters for apply command")
      
    
    if command is "job_work":
      #Work at the players job
      #Currently working takes 1 hour
      time_cost = -1
      if parameters:
        if set(['player']).issubset(parameters):
          player = parameters['player']
          if player.attributes['time'].get() >= abs(time_cost):
            player.attributes['money'].set(delta=player.job.pay)
            print "You've earned $%s" % (player.job.pay)
            player.attributes['time'].set(delta=time_cost)
          else:
            print "No time is left for work!"
        else:
          self.log_error("Inavlid parameters for work command")
      else:
        self.log_error("Inavlid parameters for work command")
    
    if command is "end":
      #End Turn
      return True
    
    if command is "course_enroll":
      #Take a class
      if parameters:
        if set(['player','course_choice']).issubset(parameters):
          if parameters['course_choice'] != '' and parameters['course_choice'] != None:
            player = parameters['player']
            self.log_debug("Looking up course %s in %s" % (parameters['course_choice'],player.location.name))
            course = player.location.get_course_by_number(parameters['course_choice'])
            self.log_debug("Course %s being taken" % (course.name))
            if course:
              #Each class has a time attribute for how long that class takes
              time_cost = course.time
              if player.attributes['time'].get() >= abs(time_cost):
                #Check if the player has enough money to pay for the course
                if player.attributes['money'].get() >= abs(course.cost):
                  self.log_debug("Player %s taking course %s at %s" % (player,course.name,player.location.name))
                  player.attributes['knowledge'].set(delta=course.knowledge_value)
                  player.completed_education.append(course.name)
                  self.log_debug("Player %s now has knowledge %s" % (player,player.attributes['knowledge'].get()))
                  player.attributes['money'].set(delta=course.cost)
                  player.attributes['time'].set(delta=time_cost)
                else:
                  print "You don't have enough money to enroll in this course!"
              else:
                print "You don't have enough time left to take this course!"
            else:
              self.log_error("Course %s not found in %s" % (parameters['course_choice'],player.location.name))
        else:
          self.log_error("Inavlid parameters for course_enroll command")
    
    if command is "item_buy":
      if parameters:
        if set(['player','item']).issubset(parameters):
          item = parameters['item']
          player = parameters['player']
          if item in player.location.items:
            if player.attributes['money'].get() >= abs(item.cost):
              player.add_item(player.location.get_item(id=item.id,delete=True))
              self.log_debug("Moved item (%s) from location (%s) to player (%s)" % (item,player,player.location))
              player.attributes['money'].set(delta=item.cost)
            else:
              print "You don't have enough money for this item"
          else:
            self.log_error("Item (%s) not found in location (items: %s)" % (item,str(player.location.items)))
        else:
          self.log_error("Invalid parameters for %s. Parameters received as %s" % (command,str(parameters)))
      else:
        self.log_error("No parameters received for %s, but they were expected" % command)
    
    if command is "item_use":
      if parameters and set(['player','item']).issubset(parameters):
        item = parameters['item']
        player = parameters['player']
        self.log_debug("Player item list: %s" % (str(player.items)))
        self.log_debug("Player item list (id): %s" % ([x.id for x in player.items]))
        self.log_debug("ID of item: %s" % item.id)
        if item in player.items:
          #use the item
          self.log_debug("Consuming item (%s) with effects %s" % (str(item),str(item.effects)))
          player.use_item(item)
          self.log_debug("Player attributes are now {%s}" % (", ".join(["%s: %s" % (key,player.attributes[key].get()) for (key,value) in player.attributes.items()])))
        else:
          self.log_error("This item (%s) does not belong to this player (%s)" % (str(item),str(player)))
    
    #If we got here, then something didn't execute correctly
    return False
