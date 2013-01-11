from uuid import uuid4

class Game:
  def __init__(self):
    self._id = uuid4()
  
  @property
  def id(self):
    """The string representation of the unique ID should be sufficient for anything using the game object to determine which game this is."""
    str(self._id)
  
