
class Menu:
  def __init__(self):
    self.title = None
    self.options = dict()
    self.indent = 2
  
  def display(self):
    """Show the menu to the user and return their selection."""
    if self.title:
      print self.title
      print '=' * len(self.title)
    if self.options:
      for key,value in self.options.iteritems():
        print "%s. %s" % (key,value)
  
class MainMenu(Menu):
  def __init__(self):
    self.title = "Main Menu"
    self.options = {'n':'New Game','q':'Quit'}
  
