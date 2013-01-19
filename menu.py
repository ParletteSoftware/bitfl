
class Menu(object):
  def __init__(self):
    self.title = None
    self.options = dict()
    self.indent = 2
    self.getch = _Getch()
  
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
        selected = self.getch()
        print "\n"
        if selected in self.options:
          return selected
        elif selected == "?":
          pass
        else:
          print "Invalid Option\n"
  
class MainMenu(Menu):
  def __init__(self):
    Menu.__init__(self)
    self.title = "Main Menu"
    self.options = {'n':'New Game','q':'Quit'}
  
class NewGameMenu(Menu):
  def __init__(self):
    Menu.__init__(self)
    self.title = "New Game Menu"
    self.options = {'a':'Add Player','l':'List Players','s':'Start Game','q':'Quit'}

class TurnMenu(Menu):
  def __init__(self):
    Menu.__init__(self)
    self.title = "Turn Menu"
    self.options = {'m':'Move','e':'End Turn','q':'Quit'}
  
  def display(self,turn_number,player_name):
    self.title = "Turn Menu: %s: Turn %s" % (player_name,turn_number)
    return super(TurnMenu,self).display()

## {{{ http://code.activestate.com/recipes/134892/ (r2)
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

## end of http://code.activestate.com/recipes/134892/ }}}
