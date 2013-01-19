from uuid import uuid4
from menu import NewGameMenu
from menu import TurnMenu
from player import Player
from map import Map
from turn import Turn

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
    #List of Turns (See Turn class)
    self.turns = list()
  
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
        selection = menu.display(len(self.turns),player.name)
        if selection == 'q':
          return True
        if selection == 'e':
          pass
      self.new_turn()
  
  def new_turn(self):
    """Create a new turn and add it to the end of the turns list."""
    if len(self.turns) > 0:
      #End the current turn
      self.turns[-1].end()
    
    #Create the next turn
    new_turn = Turn()
    self.turns.append(new_turn)
  
  def command(self,command,player):
    """Process a command for a player.
    
    Return a boolean on if the command completed successfully."""
    
    # Parameters need to be provided
    if command is None or player is None:
      return False
    
    # Parameters need to be valid
    if player not in self.players or  command not in self.commands:
      return False
    
    if command is "move":
      #Move Player
      return True
    
    if command is "end":
      #End Turn
      return True
    
    #If we got here, then something didn't execute correctly
    return False
