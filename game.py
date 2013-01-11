from uuid import uuid4
from menu import NewGameMenu
from player import Player

class Game:
  def __init__(self):
    self._id = uuid4()
    #Has the game been started?
    self.started = False
    #List of player objects
    self.players = list()
  
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
