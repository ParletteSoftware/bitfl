
class Menu(object):
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
      def print_menu():
        for key,value in sorted(self.options.iteritems()):
          print "%s. %s" % (key,value)
      while True:
        print_menu()
        selected = raw_input("> ")
        if selected in self.options:
          return selected
        elif selected == "?":
          pass
        else:
          print "Invalid Option\n"
  
class MainMenu(Menu):
  def __init__(self):
    self.title = "Main Menu"
    self.options = {'n':'New Game','q':'Quit'}
  
class NewGameMenu(Menu):
  def __init__(self):
    self.title = "New Game Menu"
    self.options = {'a':'Add Player','l':'List Players','s':'Start Game','q':'Quit'}

class TurnMenu(Menu):
  def __init__(self):
    self.title = "Turn Menu"
    self.options = {'m':'Move','e':'End Turn','q':'Quit'}
  
  def display(self,turn_number):
    self.title = "Turn Menu: Turn %s" % (turn_number)
    super(TurnMenu,self).display()
