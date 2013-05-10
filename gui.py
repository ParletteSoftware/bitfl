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
    self.version = None
    with open('version_history.txt', 'r') as f:
      self.version = f.readline()[:-1]
    
    #D - Display configuration
    self.screen = pygame.display.set_mode((1024,768))
    pygame.display.set_caption("Billy in the Fat Lane")
    
    #E - Entities (background for now)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color('black'))
    
    self.infobox = InfoBox(self.screen, Rect(0, self.screen.get_height()*.9, self.screen.get_width(), 
                          self.screen.get_height()*.1), border_width=2, border_color=Color('yellow'), font=('verdana', 16))
    self.optionsbox = OptionsBox(self.screen, Rect(self.screen.get_width()*.9, 0, self.screen.get_width()*.1, 
                               self.screen.get_height()*.9), border_width=2, border_color=Color('red'), 
                               font=('verdana', 16))
    self.mapbox = MapBox(self.screen, Rect(0, 0, self.screen.get_width()*.9, self.screen.get_height()*.9), 
                         border_width=2, border_color=Color('green'), font=('verdana', 16))
    
    #A - Action (broke this down into ALTER steps)
    # Bring up window with background drawn
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()
    
  
class GuiMainMenu(Gui):
  def welcome_message(self, version):
    line = "Welcome to Billy in the Fat Lane v"+version+"\n"
    font = pygame.font.SysFont(*('verdana', 16))
    font_color = Color('white')
    bgcolor = Color('black')
    line_sf = font.render(line, True, font_color, bgcolor)
    
    x_pos = self.screen.get_width()/2 - line_sf.get_width()/2
    y_pos = self.screen.get_height()*.1
    self.screen.blit(line_sf, (x_pos, y_pos))
    #Should there be a pygame.display.flip() here?
  
  def display(self):
    self.mainmenubox = MainMenuBox(self.screen, Rect(self.screen.get_width()*.3, self.screen.get_height()*.3,
                                  self.screen.get_width()*.4, self.screen.get_height()*.4), 
                                  border_width=2, border_color=Color('green'), font=('verdana', 16))
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
    		elif event.type == pygame.KEYDOWN:
    		  if event.key == pygame.K_ESCAPE:
    		    keepGoing = False
    		  elif event.key == pygame.K_q:
    		    return 'q'
    		  elif event.key == pygame.K_n:
    		    return 'n'
    		elif event.type == pygame.MOUSEBUTTONDOWN:
    		  current_position = pygame.mouse.get_pos()
    		  if self.mainmenubox.new_game_button.inner_rect.collidepoint(current_position):
    		    return 'n'
    		  elif self.mainmenubox.quit_button.inner_rect.collidepoint(current_position):
    		    return 'q'
	    
    	##R - Refresh display
    	self.screen.blit(self.background, (0,0))
    	self.welcome_message(self.version)
    	self.mainmenubox.draw()
    	pygame.display.flip()
    
    #end of main game loop
    
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
    	self.optionsbox.draw()
    	self.mapbox.draw(testMap)
    	pygame.display.flip()
    
    #end of main game loop
  
  

class BaseBox:
  #Base class for any box on the screen, this probably shouldn't ever be directly called
  def __init__(self, surface, rect, font=('arial', 20), font_color=Color('white'), text="Text!",
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
    self.text = text
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
            x_pos += 200
            y_pos = self.inner_rect.top
        
        self.surface.blit(line_sf, (x_pos, y_pos))
        y_pos += line_sf.get_height()
  

class OptionsBox(BaseBox):
  #The options for the player along the right of the screen
  def draw(self):
    # Border drawing
    self.draw_border()
        
    x_pos = self.inner_rect.left
    y_pos = self.inner_rect.top
    
    #Make buttons
    buttons = []
    move_button = ButtonBox(self.surface, Rect(x_pos, y_pos, self.inner_rect.width, self.inner_rect.height*.1), 
                         border_width=2, border_color=Color('gray'), font=('verdana', 12), text="Move Player",
                         bgcolor=Color('white'), font_color=Color('black'))
    buttons.append(move_button)
    y_pos += self.inner_rect.height*.1
    work_button = ButtonBox(self.surface, Rect(x_pos, y_pos, self.inner_rect.width, self.inner_rect.height*.1), 
                         border_width=2, border_color=Color('gray'), font=('verdana', 12), text="Work At Job",
                         bgcolor=Color('white'), font_color=Color('black'))
    buttons.append(work_button)
    y_pos += self.inner_rect.height*.1
    buy_item_button = ButtonBox(self.surface, Rect(x_pos, y_pos, self.inner_rect.width, self.inner_rect.height*.1), 
                         border_width=2, border_color=Color('gray'), font=('verdana', 12), text="Buy Item",
                         bgcolor=Color('white'), font_color=Color('black'))
    buttons.append(buy_item_button)
    
    for button in buttons:
      button.draw()
  

class MapBox(BaseBox):
  #The Map in the upper left
  def draw(self, map):
    # Border drawing
    self.draw_border()
        
    x_pos = self.inner_rect.left
    y_pos = self.inner_rect.top
    
    #Draw the map
    for row in map.grid:
      s = ''
      for point in row:
        s += " %s " % str(point) if point else " - "
      line_sf = self.font.render(s, True, self.font_color, self.bgcolor)
      self.surface.blit(line_sf, (x_pos, y_pos))
      y_pos += line_sf.get_height()
  

class ButtonBox(BaseBox):
  #Individual options button
  def draw(self):
    self.draw_border()
    
    line_sf = self.font.render(self.text, True, self.font_color, self.bgcolor)
    x_pos = self.inner_rect.centerx - (line_sf.get_width()/2)
    y_pos = self.inner_rect.centery - (line_sf.get_height()/2)
    self.surface.blit(line_sf, (x_pos, y_pos))
  

class MainMenuBox(BaseBox):
  #Choices presented at the main menu, currently New Game and Quit
  def draw(self):
    self.draw_border()
    
    x_pos = self.inner_rect.left
    y_pos = self.inner_rect.top
    
    #Make buttons
    self.buttons = []
    self.new_game_button = ButtonBox(self.surface, Rect(x_pos, y_pos, self.inner_rect.width, self.inner_rect.height*.1), 
                         border_width=2, border_color=Color('gray'), font=('verdana', 12), text="(N)ew Game",
                         bgcolor=Color('white'), font_color=Color('black'))
    self.buttons.append(self.new_game_button)
    y_pos += self.inner_rect.height*.1
    self.quit_button = ButtonBox(self.surface, Rect(x_pos, y_pos, self.inner_rect.width, self.inner_rect.height*.1), 
                         border_width=2, border_color=Color('gray'), font=('verdana', 12), text="(Q)uit Game",
                         bgcolor=Color('white'), font_color=Color('black'))
    self.buttons.append(self.quit_button)
    for button in self.buttons:
      button.draw()
    
    