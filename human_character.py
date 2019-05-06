import pygame
import pygame.gfxdraw

import math, time
import human_n_articulation
from human_n_articulation import *

		
class human_character(object):
	def __init__(self, surface = None, prospective="back", position=None, on={"AG":True, "AF":True, "CE":True, "CD":True}):
		self.surface = surface
		self.prsp = prospective
		self.position = position   #[x, y]
		self.on = on
		self.b = human_articulation(position=(position[0], position[1]+40), angle=90, direction = "right")
		
		bpoints = self.b.points
		self.a = human_articulation(position=(bpoints[0][0], bpoints[0][1]), angle=90, clockwise=False)
		
		
		self.ce1 = human_articulation(position=(position[0], position[1]+240), angle=45, clockwise=False)
		self.ce2 = human_articulation(position=(position[0], position[1]+240), angle=90, clockwise=False)
		self.CE = self.ce1 +self.ce2
		
		self.cd1 = human_articulation(position=(position[0], position[1]+240), angle=90+45, clockwise=False)
		self.cd2 = human_articulation(position=(position[0], position[1]+240), angle=90, clockwise=True, direction="left")
		self.CD = self.cd1 + self.cd2
		
		
		#--------braccia---
		
		self.af1 = human_articulation(position=(position[0], position[1]+40), angle=90+60, clockwise=False)
		self.af2 = human_articulation(position=(position[0], position[1]+40), angle=90, clockwise=False)
		self.AF = self.af1 + self.af2
		
		self.ag1 = human_articulation(position=(position[0], position[1]+40), angle=30, clockwise=False)
		self.ag2 = human_articulation(position=(position[0], position[1]+40), angle=90, clockwise=False)
		self.AG = self.ag1 + self.ag2
		
#tupset [ [line1] [line2] ]
													 #line1/2 array : [ [coord1] [coord2] ]
													 #coord structure : [x,y] 
	def draw(self, font=None): #on = {"AG":true, "Af":True, "CE":True, "CD":True}
		def sub_draw(surface,tup_set, font_text="-", reverse = False): 
			for x in range(len(tup_set)):
				pygame.gfxdraw.line(surface, tup_set[x][0][0], tup_set[x][0][1], tup_set[x][1][0], tup_set[x][1][1], (30,58,96))  #parte superiore colonna vertebrale
				pygame.gfxdraw.filled_circle(surface, tup_set[x][1][0], tup_set[x][1][1], 4,(0,0,0)) if (reverse == False) else pygame.gfxdraw.filled_circle(surface, tup_set[x][0][0], tup_set[x][0][1], 4,(0,0,0))
			if(font !=None):
				text = font.render(str(font_text), True, (65,105,225))
				surface.blit(text, (tup_set[0][1][0]+5,tup_set[0][1][1])) if (reverse == False) else surface.blit(text, (tup_set[0][0][0]+5,tup_set[0][0][1]))
    
			
		aSet = self.a.points
		bSet = self.b.points
		self.CE.set_anchor((aSet[1][0], aSet[1][1]))
		CESet = self.CE.get_set()
		
		self.CD.set_anchor((aSet[1][0], aSet[1][1]))
		CDSet = self.CD.get_set()
		
		temp= self.b._calculate_line(length=self.b.length, angle=self.b.angle, dirc = self.b._get_direction()) 
		pygame.gfxdraw.aacircle(self.surface, temp[0], temp[1], 30, (0,0,0))#testa
		self.AF.set_anchor(self.b._calculate_line(length=40, angle=self.b.angle, dirc = self.b._get_direction()) )
		self.AG.set_anchor(self.b._calculate_line(length=40, angle=self.b.angle, dirc = self.b._get_direction()) )
		
		AFSet = self.AF.get_set()
		
		AGSet = self.AG.get_set()
		
		#pygame.gfxdraw.line(surface, aSet[0][0], aSet[0][1], aSet[1][0], aSet[1][1], (30,58,96))  #parte superiore colonna vertebrale
		#pygame.gfxdraw.line(surface, bSet[0][0], bSet[0][1], bSet[1][0], bSet[1][1], (30,58,96))  #parte superiore colonna vertebrale
		
		sub_draw(self.surface, (bSet,), font_text = self.b.get_angle(), reverse = True)
		sub_draw(self.surface, (aSet,), font_text = self.AF.get_angle())

#	<expression1> if <condition> else <expression2>

		if (self.on["CE"] == True) : sub_draw(self.surface, CESet, font_text = self.CE.get_angle()) 
		if (self.on["CD"] == True) : sub_draw(self.surface, CDSet, font_text = self.CD.get_angle()) 
		if (self.on["AF"] == True) : sub_draw(self.surface, AFSet, font_text = self.AF.get_angle()) 
		if (self.on["AG"] == True) : sub_draw(self.surface, AGSet, font_text = self.AG.get_angle())
		
	def animation(self, node, line, angle):
		if(node == 'B'):#complicato
			if ( angle < 90 ):
				self.b.direction = "right"
				self.b.animation(angle)
			elif ( angle >= 90):
				self.b.direction = "left"
				self.b.animation(180+angle)	
		if(node == 'D'):
			self.CD.animation(line=line, angle=angle)
		elif(node == 'E'):
			self.CE.animation(line=line, angle=angle)
		elif(node == 'F'):
			self.AF.animation(line=line, angle=angle)
		elif(node == 'G'):
			self.AG.animation(line=line, angle=angle)

		
"""

pygame.init()

clock = pygame.time.Clock()
clock.tick(60)
size=[800, 800]
global screen
surface = pygame.display.set_mode(size)

dead=False


global positionMove
positionMove=0

hum1 = human_character(surface, position=[200, 100], on = {"AG":True, "AF":True, "CE":True, "CD":True})
hum2 = human_character(surface, position=[500, 100])

font = pygame.font.SysFont("arial", 15, bold=True)
while(dead==False):
	for x in range(0,90):
		hum1.animation(node="E", line="main", angle=x)
		hum1.animation(node="G", line="-", angle=x)
		hum1.animation(node="D", line="main", angle=90+x)
		hum2.animation(node="B", line="main", angle=x*2)
		hum2.animation(node="B", line="", angle=x)
		hum1.draw(font=font)
		hum2.draw(font=font)
		pygame.display.flip()
		surface.fill((255,255,255))
		time.sleep(0.03)

pygame.display.quit()
"""
