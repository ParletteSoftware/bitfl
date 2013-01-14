from uuid import uuid4

class Turn:
  def __init__(self):
    self.id = uuid4()
    #Is this turn active?
    self.active = True
  
  def end(self):
    """Perform any end of turn functions to each player."""
    self.active = False
  
  def add(self,event = None):
    if self.event:
      pass
    return False
