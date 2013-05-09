"""Billy in the Fat Lane - A Lame Life Simulation Game
Copyright (C) 2013 Chris Parlette, Matt Parlette

This file is part of Billy in the Fat Lane.

Billy in the Fat Lane is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Billy in the Fat Lane is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Billy in the Fat Lane.  If not, see http://www.gnu.org/licenses/."""

class Menu(object):
  def __init__(self):
    self.title = None
    self.options = dict()
    self.indent = 2
    self.getch = _Getch()
    self.allow_cancel = False
  
  def display(self,sort = True):
    """Show the menu to the user and return their selection."""
    if self.title:
      print self.title
      print '=' * len(self.title)
    if self.options:
      def print_menu():
        #Print the list, either sorted or just as is
        if sort:
          for key,value in sorted(self.options.iteritems()):
            print "%s. %s" % (key,value)
        else:
          for key,value in self.options.iteritems():
            print "%s. %s" % (key,value)
        if self.allow_cancel:
          print "(Enter to cancel)"
      while True:
        print_menu()
        selected = self.getch()
        print "\n"
        if selected in self.options:
          return selected
        elif selected == "\r" and self.allow_cancel:
          return ''
        elif selected == "?":
          pass
        else:
          print "Invalid Option\n"
    else:
      print "No options available!\n"
  
  def add_option(self,key,value):
    """Add an option to the menu.
    
    The key is a character the player can use to select this option. The value is a friendly name for this option."""
    
    if key not in self.options:
      self.options[key] = value
  
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
    self.options = {'m':'Move','e':'End Turn','q':'Quit','i':'Player Info'}
  
  def display(self,turn_number,player,time_left):
    self.title = "Turn Menu: %s: Turn %s\nTime Left: %s hours\nLocation: %s" % (player.name,turn_number,time_left,player.location.name)
    return super(TurnMenu,self).display()

class MoveMenu(Menu):
  def __init__(self,locations):
    super(MoveMenu,self).__init__()
    self.title = "Move Player"
    self.options = {}
    #Build the options from the locations list
    for location in locations:
      self.options[location.symbol] = location.name
    
    #We want the user to be able to cancel
    self.allow_cancel = True
  
  def display(self,map):
    print map
    return super(MoveMenu,self).display()

class JobMenu(Menu):
  def __init__(self):
    super(JobMenu,self).__init__()
    self.title = "Job Menu"
    self.options = {}
  
  def display(self,job = None,job_list = None):
    if job and job_list:
      print "Error in JobMenu.display(): job and job_list cannot both be provided"
      return None
    
    if job:
      self.title = "Job Menu: %s" % job.name
      self.options = {'w':'Work','q':'Quit'}
    
    if job_list:
      self.title = "Apply for job"
      for j in job_list:
        self.options[str(j.rank)] = "%s ($%s pay per unit)" % (j.name,str(j.pay))
      self.allow_cancel = True
    
    return super(JobMenu,self).display(sort=True)

class CourseMenu(Menu):
  def __init__(self):
    super(CourseMenu,self).__init__()
    self.title = "Education Menu"
    self.options = {}
  
  def display(self,course_list, player):
    self.title = "Enroll in a course"
    for c in course_list:
      #Check if the player has the knowledge required, class required, or has already taken the course
      player_can_take_course = True
      if player.knowledge < c.knowledge_required:
        player_can_take_course = False
      if c.course_required:
        if c.course_required not in player.completed_education:
          player_can_take_course = False
      if c.name in player.completed_education:
        player_can_take_course = False
      #Add course as an option if player is qualified and hasn't already taken it
      if player_can_take_course:
        self.options[str(c.symbol)] = "%s - %s time spent - %s knowledge gained - $%s to enroll" % (c.name,str(c.time),str(c.knowledge_value),str(c.cost))
    self.allow_cancel = True
    
    return super(CourseMenu,self).display(sort=True)

class BuyMenu(Menu):
  def __init__(self):
    super(BuyMenu,self).__init__()
    self.title = "Buying An Item"
    self.options = {}
  
  def display(self,item_list):
    if item_list:
      for i in item_list:
        #We use a string representation of the index of each item
        self.options[str(item_list.index(i))] = "%s ($%s)" % (i.name,str(i.cost))
      self.allow_cancel = True
    
    selection = super(BuyMenu,self).display(sort=True)
    if selection:
      #Convert the selection from string (above) to int for lookup
      return item_list[int(selection)]

class ListMenu(Menu):
  """A generic menu that allows the user to select items from a list.
  
  Note that this returns the object in the list, not the index of that item."""
  def __init__(self,title = "List Menu",options = []):
    super(ListMenu,self).__init__()
    self.title = title
    #Convert the passed list into a dictionary
    self.options = {}
    i = 1
    for item in options:
      self.options[str(i)] = item
      i += 1
  
  def display(self):
    """Return the object from the list rather than the index of that item."""
    return self.options[super(ListMenu,self).display(sort=False)]

class QuitMenu(Menu):
  def __init__(self, options={'q':'Quit BITFL completely'}):
    Menu.__init__(self)
    self.title = "Quit Menu"
    self.options = options
    self.allow_cancel = True
  
  def display(self):
    choice = super(QuitMenu, self).display(sort=False)
    if choice == 'q':
      return True, True
    elif choice == 'm':
      return False, True
    else:
      return False, False
  


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
