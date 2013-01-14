from uuid import uuid4

class Player:
  def __init__(self,name = "Player"):
    self.name = name
    self.id = uuid4()
    self.location = None
    self.turns = 0
  
  def __repr__(self):
    return str(self.name)
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  
  def move_player(self,new_location):
    """Change the player's location variable.
    The validity of this move should be done before this function is called."""
    self.location = new_location
    return True
