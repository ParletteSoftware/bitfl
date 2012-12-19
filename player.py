class Player:
  def __init__(self,name = "Player"):
    self.name = name
    self.location = None
  
  def move_player(self,new_location):
    """Change the player's location variable.
    The validity of this move should be done before this function is called."""
    self.location = new_location
    return True
