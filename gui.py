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

from uuid import uuid4
import pygame

""" mapping out the IDEA/ALTER model for pygame programming.
	I-Import and Initialize
	D-Display
	E-Entitites
	A-Action

	A-Assign values
	L-Loop
	T-Time
	E-Events
	R-Refresh screen 
	
	from http://www.gamedev.net/community/forums/topic.asp?topic_id=444490 """

class Gui:
  def __init__(self):
    #I - Import and Initialize
    pygame.init()
    
    #D - Display configuration
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Billy in the Fat Lane")
    
    #E - Entities (background for now)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((100,60,25))
    
    #A - Action (broke this down into ALTER steps)
  
  def run(self):
    ##A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    
    ##L - Main Loop
    while keepGoing:
    	##T - Timer to set frame rate
    	clock.tick(30)
	    
    	##E - Event handling
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			keepGoing = False
	    
    	##R - Refresh display
    	screen.blit(background, (0,0))
    	pygame.display.flip()
    
    #end of main game loop
  
  
