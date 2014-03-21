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

from menu import MainMenu, QuitMenu
from game import Game
from map import Map
import os
import argparse

version = None
with open('version_history.txt', 'r') as f:
  version = f.readline()[:-1]

parser = argparse.ArgumentParser(description='Process command line options.')
parser.add_argument('--debug', action='store_true', help='Turn on debug logging')
parser.add_argument('--version', action='version', version='Billy in the Fat Lane v'+version)
args = parser.parse_args()

quit_completely = False
main_menu = MainMenu()

while not quit_completely:
  """Clear the screen, use cls if Windows or clear if Linux"""
  if not args.debug:
    os.system('cls' if os.name=='nt' else 'clear')
  print "Welcome to Billy in the Fat Lane v"+version+"\n"
  selection = main_menu.display().lower()
  """Clear the screen, use cls if Windows or clear if Linux"""
  if not args.debug:
    os.system('cls' if os.name=='nt' else 'clear')
  if selection == 'q':
    quit_completely, quit_to_main_menu = QuitMenu().display()
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
        game = Game(map_list[0], debug=args.debug)
      game_started = False
      game_started, quit_completely = game.start()
      if game_started and not quit_completely:
        quit_completely = game.run()
    else:
      print "...no maps found"
