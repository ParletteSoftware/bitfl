from menu import MainMenu
from game import Game

done = False
main_menu = MainMenu()

while not done:
  print "Welcome to Billy in the Fat Lane"
  selection = main_menu.display().lower()
  if selection == 'q':
    done = True
  if selection == 'n':
    print "Starting new game..."
    game = Game()
    game.start()
