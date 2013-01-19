from uuid import uuid4

class Location:
  def __init__(self,name = "Location"):
    self.name = name
    self.id = uuid4()
    self.jobs = []
  
  def __eq__(self,other):
    return self.id == other.id if hasattr(other,"id") else False
  

