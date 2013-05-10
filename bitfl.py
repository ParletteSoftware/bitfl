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

from menu import MainMenu
from game import Game
from map import Map
import os
import argparse
from gui import Gui, GuiMainMenu

version = None
with open('version_history.txt', 'r') as f:
  version = f.readline()[:-1]

def clear_screen():
  """Clear the screen, use cls if Windows or clear if Linux"""
  if not args.debug:
    os.system('cls' if os.name=='nt' else 'clear')

parser = argparse.ArgumentParser(description='Process command line options.')
parser.add_argument('--debug', action='store_true', help='Turn on debug logging')
parser.add_argument('--version', action='version', version='Billy in the Fat Lane v'+version)
parser.add_argument('--gui', action='store_true', help='Enable the Pygame GUI')
parser.add_argument('--cli', action='store_true', help='Enable the Command Line Interface')
args = parser.parse_args()

if args.gui:
  main_menu = GuiMainMenu()
elif args.cli:
  main_menu = MainMenu()
else:
  #Default to CLI, but this else block is here so we can present a choice if they didn't pick
  main_menu = MainMenu()

done = False
while not done:
  clear_screen()
  #print "Welcome to Billy in the Fat Lane v"+version+"\n"
  main_menu.welcome_message(version)
  selection = main_menu.display().lower()
  clear_screen()
  if selection == 'q':
    done = True
  if selection == 'n':
    print "Loading maps..."
    map_list = []
    if os.path.exists("maps"):
      maps_dir = os.path.join(os.path.dirname(__file__),"maps")
      for map_dir in [name for name in os.listdir(maps_dir) if os.path.isdir(os.path.join(maps_dir, name))]:
        map_list.append(Map(os.path.join(maps_dir,map_dir),debug=args.debug))
        print "loaded %s" % (map_list[-1].title)
    if len(map_list):
      print "...done"
      print "Starting new game..."
      if len(map_list) == 1:
        game = Game(map_list[0], debug=args.debug, gui=args.gui)
      if game.start():
        game.run()
    else:
      print "...no maps found"
