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
from pygame import Rect, Color
from player import Player
from map import Map
import os

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
    self.screen = pygame.display.set_mode((1024,768))
    pygame.display.set_caption("Billy in the Fat Lane")
    
    #E - Entities (background for now)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color('black'))
    
    self.infobox = InfoBox(self.screen, Rect(0, self.screen.get_height()*.9, self.screen.get_width(), 
                          self.screen.get_height()*.1), border_width=2, border_color=Color('yellow'), font=('verdana', 16))
    
    #A - Action (broke this down into ALTER steps)
  
  def run(self):
    ##A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    #import maps, this is just a test right now
    map_list = []
    maps_dir = os.path.join(os.path.dirname(__file__),"maps")
    for map_dir in [name for name in os.listdir(maps_dir) if os.path.isdir(os.path.join(maps_dir, name))]:
      map_list.append(Map(os.path.join(maps_dir,map_dir)))
    testMap = map_list[0]
    #create a player to test
    player = Player('testPlayer')
    player.move(testMap.locations[0])
    
    ##L - Main Loop
    while keepGoing:
    	##T - Timer to set frame rate
    	clock.tick(30)
	    
    	##E - Event handling
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			keepGoing = False
    		elif event.type == pygame.KEYDOWN:
    		  if event.key == pygame.K_ESCAPE:
    		    keepGoing = False
	    
    	##R - Refresh display
    	self.screen.blit(self.background, (0,0))
    	self.infobox.draw(player.info_display().split('\n'))
    	pygame.display.flip()
    
    #end of main game loop
  
  

class BaseBox:
  #Base class for any box on the screen, this probably shouldn't ever be directly called
  def __init__(self, surface, rect, font=('arial', 20), font_color=Color('white'),
               bgcolor=Color('gray25'), border_width=0, border_color=Color('black')):
    """ rect: The (outer) rectangle defining the location and size of the box on the surface.
        bgcolor: The background color
        border_width: Width of the border. If 0, no border is drawn. If > 0, the border 
            is drawn inside the bounding rect of the widget (so take this into account when
            computing internal space of the box).
        border_color: Color of the border.
        text: The initial text of the message board.
        font: The font (a name, size tuple) of the message
        font_color: The font color
    """
    self.surface = surface
    self.rect = rect
    self.bgcolor = bgcolor
    self.font = pygame.font.SysFont(*font)
    self.font_color = font_color
    self.border_width = border_width
    self.border_color = border_color
    # Internal drawing rectangle of the box 
    self.inner_rect = Rect(self.rect.left + self.border_width, self.rect.top + self.border_width,
        self.rect.width - self.border_width * 2, self.rect.height - self.border_width * 2)
  
  def draw_border(self):
    # Border drawing
    pygame.draw.rect(self.surface, self.border_color, self.rect)
    pygame.draw.rect(self.surface, self.bgcolor, self.inner_rect)
    
class InfoBox(BaseBox):
  #The stats of the current player along the bottom of the screen
  def draw(self, text):
    # Border drawing
    self.draw_border()
        
    x_pos = self.inner_rect.left
    y_pos = self.inner_rect.top 
    
    # Render all the lines of text one below the other
    for line in text:
        line_sf = self.font.render(line, True, self.font_color, self.bgcolor)
        
        if (line_sf.get_width() + x_pos > self.rect.right or line_sf.get_height() + y_pos > self.rect.bottom):
            print 'Cannot fit line "%s" in InfoBox, moving to the right' % line
            x_pos += 200
            y_pos = self.inner_rect.top
        
        self.surface.blit(line_sf, (x_pos, y_pos))
        y_pos += line_sf.get_height()
  

class ButtonBox(BaseBox):
  #The options for the player along the right of the screen
  def draw(self, text):
    # Border drawing
    self.draw_border()
        
    x_pos = self.text_rect.left
    y_pos = self.text_rect.top
    
    #Make buttons