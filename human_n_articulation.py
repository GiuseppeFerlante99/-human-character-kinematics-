import math
class human_articulation(object):
	def __init__(self, position=None, angle=None, clockwise = True, direction="left"):
		self.pos = position 
		self.points = None
		self.angle = angle
		self.clockwise = clockwise
		self.direction = direction
		self.create_articulation(direction)
		self.length = 100#dopo viene modificata 
		
		
	def _calculate_line(self, length, angle, dirc ):
		angle_rad= angle * 0.0174533
		return [self.pos[0]+int(math.cos(angle_rad)*length*dirc),  
		        self.pos[1]+int(math.sin(angle_rad)*length*dirc)]
	def _get_direction(self, direction=None):
		for x in range(0,2):
			if(direction == "left"): return 1
			elif(direction=="right"): return -1
			else:
				direction = self.direction


	def create_articulation(self, direction=None, length = 70):
		self.length = length
		dirc = self._get_direction(direction)
		points_temp_xy2 = self._calculate_line( length = length, angle = self.angle, dirc = dirc)
		#self.points = [(self.pos[0], self.pos[1]),(self.pos[0]+int(math.cos(angle_rad)*length*dirc), self.pos[1]+int(math.sin(angle_rad)*length*dirc))]
		self.points = [(self.pos[0], self.pos[1]),(points_temp_xy2[0], points_temp_xy2[1])]
		return self
		
	def animation(self, angle = None):
		self.angle = angle
		self.create_articulation(self.direction)
	def get_points(self):
		return self.points
	def get_angle(self):
		if(self.direction=="right"):
			return self.angle-90
		else:
			return self.angle-270
	
	def __add__(self, other):
		return n_articulation_welded().weld(self, other)

class n_articulation_welded(object): 
	def __init__(self):
		self.obj1 = None
		self.obj2 = None
	def weld(self, obj1, obj2):
		self.obj1 = obj1
		self.obj2 = human_articulation(position = obj1.points[1], angle=obj2.angle, clockwise = obj2.clockwise, direction = obj2.direction) 
		self.obj2.create_articulation()
		return self
	def get_set(self):
		return [self.obj1.points, self.obj2.points]
	def animation(self,line="main", angle=None):
		if(line=="main"):
			self.obj1.angle=angle
			self.obj1.create_articulation()
			self.weld(self.obj1, self.obj2)
		else:
			self.obj2.angle = angle
			self.obj2.create_articulation() 
	def get_angle(self):
		if(self.obj1.angle <= 90 ):
			return  self.obj2.angle-self.obj1.angle
		else:
			return self.obj1.angle - self.obj2.angle	
	def set_anchor(self, new_pos):
		self.obj1 = human_articulation(position = new_pos, angle = self.obj1.angle, clockwise = self.obj1.clockwise)
		self.obj1.create_articulation() 
		self.weld(self.obj1, self.obj2)

		
