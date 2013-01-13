from uuid import uuid4

class Player:
  def __init__(self,name = "Player"):
    self.name = name
    self._id = uuid4()
    self.location = None
    self.turns = 0
  
  @property
  def id(self):
    """The string representation of the unique ID should be sufficient for anything using the game object to determine which game this is."""
    str(self._id)
  
  def move_player(self,new_location):
    """Change the player's location variable.
    The validity of this move should be done before this function is called."""
    self.location = new_location
    return True
