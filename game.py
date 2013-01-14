from uuid import uuid4
from menu import NewGameMenu
from player import Player
from map import Map

class Game:
  def __init__(self):
    self._id = uuid4()
    #Valid commands this game class will accept
    self.commands = ["move","end"]
    #Has the game been started?
    self.started = False
    #List of player objects
    self.players = list()
    #Game Board
    self.map = Map()
  
  @property
  def id(self):
    """The string representation of the unique ID should be sufficient for anything using the game object to determine which game this is."""
    str(self._id)
  
  def start(self):
    menu = NewGameMenu()
    
    #Display the menu until the user quits or starts the game
    while True:
      selection = menu.display().lower()
      if selection == 'q':
        break
      if selection == 's':
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
  
  def command(self,command = None,player = None):
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
