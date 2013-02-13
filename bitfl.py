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

parser = argparse.ArgumentParser(description='Process command line options.')
parser.add_argument('--debug', action='store_true', help='Turn on debug logging')
parser.add_argument('--version', action='store_true', help='Display the current version')
args = parser.parse_args()

done = False
main_menu = MainMenu()

while not done:
  """Clear the screen, use cls if Windows or clear if Linux"""
  if not args.debug:
    os.system('cls' if os.name=='nt' else 'clear')
  print "Welcome to Billy in the Fat Lane"
  if args.version:
    f = open('version_history.txt', 'r')
    print "The current version is " + f.readline()
    f.close()
  selection = main_menu.display().lower()
  """Clear the screen, use cls if Windows or clear if Linux"""
  if not args.debug:
    os.system('cls' if os.name=='nt' else 'clear')
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
        game = Game(map_list[0], debug=args.debug)
      if game.start():
        game.run()
    else:
      print "...no maps found"
