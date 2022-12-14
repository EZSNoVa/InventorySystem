from typing import List
import pygame as pg, random
from ..objects import Object, Group, Circle, Rect, Text
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core import grid
from pathfinding.finder.a_star import AStarFinder
from ..primitive_objects import PRect

class IObject:
	@staticmethod
	def extend(object):
		
		iobject = IObject(object)
		
		for k in dir(iobject):
			if k not in ["size", "pos", "id"] and not k.startswith("__"):
				setattr(object, k, getattr(iobject, k))
		
		return object
	
	def __init__(self, object):

		self.object = object
		self.screen = self.object.screen
		self.objects = Group()
		self._clicked = False

	@property
	def clicked(self):
		return self._clicked
	
	@clicked.setter
	def clicked(self, value):
		self._clicked = value
		
	def _process_click(self, func):
		self.clicked = True
		func()
        
	def click(self, func, event_name="Default"):
		self.screen.events.add_event("click", self.object, lambda: self._process_click(func), event_name)
		return func
	
	def hover(self, func, event_name="Default"):
		self.screen.events.add_event("hover", self.object, func, event_name)
		return func

	def unhover(self, func, event_name="Default"):
		self.screen.events.add_event("unhover", self.object, func, event_name)
		return func
	
	def _process_unclick(self, func):
		if self.clicked:
			self.clicked = False
			func()
			
	def unclick(self, func, event_name="Default"):
		self.screen.events.on_event("mouseup", lambda : self._process_click(func), event_name)
		return func
   

class Grid(Object):
	def __init__(self, pos, size, grid_size:List[int], **styles):
		super().__init__(pos, size, **styles)
		self.box_styles = styles.get("box_styles", {})
		self.grid_size = grid_size
		self.matrix = self.grid_div(*self.grid_size) 
		self.grid = self.grid_split(self.matrix, self.grid_size[1])
		self.colors_grid = [[obj.color for obj in row] for row in self.grid]
		  
	def div(self, axis, q):
		r'''
		Return list of division points of the screen -> [[x1, x2], [x1, x2], ...]
		'''
		divs = []
		if axis == "x":
			# should append [start, end] for each division
			for i in range(q):
				divs.append([round(i * self.size[0] / q, 1), round((i + 1) * self.size[0] / q, 1)])
		elif axis == "y":
			# should append [start, end] for each division
			for i in range(q):
				divs.append([round(i * self.size[1] / q, 1), round((i + 1) * self.size[1] / q, 1)])
			
		return divs
		
	def grid_div(self, cols=3, rows=3, transpose=False):
		r'''
		Returns the division of the screen into a grid -> [[x, y, w, h], [x, y, w, h], ...]
		'''
		grid = []
		divs_x = self.div("x", cols)
		box_width = divs_x[-1][0] - divs_x[-2][0]
		divs_y = self.div("y", rows)
		box_height = divs_y[-1][0] - divs_y[-2][0]
		self.grid_size = [rows, cols]
		
		for i in range(cols):
			for j in range(rows):
				if transpose:
					grid.append([divs_x[j][0] + self.pos[0], 
                  				divs_y[i][0] + self.pos[1], 
                     			box_width, box_height])
				else:
					grid.append([divs_x[i][0] + self.pos[0], 
                  				divs_y[j][0] + self.pos[1], 
                      			box_width, box_height])
     
		self.grid_space = len(grid)
		self.grid_box_size = [box_width, box_height]
		return grid
	
	def grid_split(self, matrix, grid_size):
		r'''
		Splits a matrix into a grid : [1,2,3,4,5,6,7,8,9] -> [[Unit,Unit,Unit], [Unit,Unit,Unit], [Unit,Unit,Unit]]
		'''
		if isinstance(grid_size, list) or isinstance(grid_size, tuple):
			grid_size = grid_size[1]
		
		grid = [matrix[i:i+grid_size] for i in range(0, len(matrix), grid_size)]
		return [[Rect(pos=i[:2], size=i[2:], **self.box_styles)  for i in row] for row in grid]
	
	def draw(self):
		screen = self.screen
		
		pg.draw.rect(screen.surface, self.color, [*self.get_pos(), *self.size], int(self.stroke))
		for row in self.grid:
			for obj in row:
				obj.draw()
			
	def highlight_current(self, color="red"):
		for i in range(len(self.colors_grid)):
			for j in range(len(self.colors_grid[i])):
				if self.colors_grid[i][j] != color:
					self.grid[i][j].color = self.colors_grid[i][j]
		
		mouse_pos = self.screen.mouse_pos()
		pos = int(mouse_pos[0] // self.grid_box_size[0]), int(mouse_pos[1] // self.grid_box_size[1])
		# select the current box
		
		if pos[0] < self.grid_size[0] and pos[1] < self.grid_size[1]:
			self.grid[pos[0]][pos[1]].color = color

	def get_path(self, start,end):
		int_grid = [[1 for x in j] for j in self.grid]
	
		_grid = grid.Grid(matrix=int_grid)
		start = _grid.node(*start)
		end = _grid.node(*end)

		finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

		path, _ = finder.find_path(start=start, end=end, grid=_grid)
		
		return path

	def highlight_path(self, start, end, color="red"):
		if  0 > (start[0] or start[1]) or start[1] > self.grid_size[1] or start[0] > self.grid_size[0]:
			raise Exception("Start position is out of bounds")
		if 0 > (end[0] or end[1]) or end[1] > self.grid_size[1] or end[0] > self.grid_size[0]:
			raise Exception("End position is out of bounds")
		if start == end:
			raise Exception("Start and end positions must be different")
		
		path = self.get_path(start, end)
		for i in range(len(path)):
			self.grid[path[i][0]][path[i][1]].color = color
	

	def get_current(self):
		mouse_pos = self.screen.mouse_pos()
		pos = int(mouse_pos[0] // self.grid_box_size[0]), int(mouse_pos[1] // self.grid_box_size[1])
		# select the current box
		if pos[0] < self.grid_size[0] and pos[1] < self.grid_size[1]:
			return self.grid[pos[0]][pos[1]]
		else:
			return None

	
def _get_object(object):
	args = {k:v for k,v in object.items() if k != "type" and  k != "elements"}
	try:
		obj = eval(object["type"].capitalize())(**args)
	except Exception as e:
		raise Exception("Could not load object: " + str(e))
				
	return obj

def _get_object_child(parent, object, childs=[]):
	for key,value in object["elements"].items():
		if "pos" in value:
			value["pos"] = [value["pos"][0] + parent.pos[0], value["pos"][1] + parent.pos[1]]
		
		parent = _get_object(value)
		childs.append(parent)
   
	for value in object["elements"].values():
		if "elements" in value:   
			_get_object_child(parent, value, childs)
	
	return childs
	
def load_custom_object(object):
	r'''
	Load a custom object from a object of json file
	'''
	obj = Group(_get_object(object))   
	obj.add(_get_object_child(obj.objects[0], object))
	return obj

class RangeBar(Object):
	def __init__(self, pos, size, min, max, value, **styles):
		for item in (min, max, value):
			if item < 0 or item > 100:
				raise ValueError(f"{item} must be between 0 and 100, at RangeBar object")
		
		super().__init__(pos=pos, size=size, **styles)
		
		radius = styles.get("radius", self.size[1] / 2.5 - self.size[1]//8)
		wheel_color = styles.get("wheel_color", "white")
		
		self.wheel = IObject(Circle(pos=[0,0], radius=radius, color=wheel_color))
		
		self.bar = Object(pos=pos, size=size, **styles)
		
		self.min = (min  * (self.pos[0]+ self.size[0])) / 100 if min != 0 else self.pos[0]
		self.max = (max * (self.pos[0]+ self.size[0])) / 100
		self.value = (value * (self.min + self.max)) / 100        
		self._evname = f"RangeBar_{self.id}_update_value_[{random.randint(0,255)}]"
		
		@self.wheel.click()    
		def wheel_click():     
			self._evname = f"RangeBar_{self.id}_update_value_[{random.randint(0,255)}]"
			self.screen.time.add(time=10, callback=self._update_value, name=self._evname) 

		@self.wheel.unclick()
		def wheel_unclick():
			if self.wheel.clicked:
				self.screen.time.remove(name=self._evname)
				self.wheel.color = "white"

	def _update_value(self):
		mouse_pos = self.screen.mouse_pos()[0]
 
		if mouse_pos + self.wheel.radius < self.min:
			self.value = self.min 
		
		elif mouse_pos + self.wheel.size[0] > self.max:
			self.value = self.max
			
		else:
			self.value = mouse_pos 
			
		self.wheel.color = "red"

	def _calculate_wheel_pos(self):
		x = self.value
		if x == self.min:
			x = self.min - self.wheel.radius /2 
			
		elif x == self.max: 
			x = self.max + self.wheel.radius /2
						
		self.wheel.pos = [x, self.pos[1]+self.size[1]//2]

	def draw(self):
		self._calculate_wheel_pos()
		Rect(pos=[self.pos[0], self.pos[1]+self.size[1]/2], size=[self.size[0]+self.wheel.radius, self.size[1]//8], color=self.color).draw()
		self.wheel.draw()
	
	def get_percent(self):
		if self.value == self.min:
			return 0
		elif self.value == self.max:
			return 100
		
		return round( (self.value / ( (self.min + self.wheel.radius) + (self.max - self.wheel.radius) ) ) * 100, 4)

class Bar(Object):
	def __init__(self, pos, size, min, max, value, **styles):
		super().__init__(pos=pos, size=size, **styles)
		
		self.min = min
		self.max = max
		self.value = value
		
		self.fill_color = styles.get("fill_color", "white")
		stroke = styles.get("stroke", 2)
		
		self.bar = Rect(pos=self.pos, size=size, color=self.color, stroke=stroke)
		self.fill_bar = Rect(pos=self.pos, size=[0, self.size[1]], color=self.fill_color)
		
	def _update_value(self):
		if self.value < self.min:
			self.value = self.min
		elif self.value > self.max:
			self.value = self.max
			
		p = (self.value * 100)/ self.max
			
		self.fill_bar.size = [(p / 100) * self.size[0], self.size[1]]


	def draw(self):
		screen = self.screen 
		
		self._update_value()
		self.fill_bar.draw()
		self.bar.draw()
		
class CheckBox(Rect):
	def __init__(self, pos, size, **styles):
		self.state = False
		styles["stroke"] = 5
		super().__init__(pos, size, **styles)

		# init 
		self.screen.events.add_event(event="mousedown", object=self, callback= self.change_state)
		self.checkbox = Rect(size=[self.size[0]/2, self.size[1]/2], pos=[self.pos[0]+self.size[0]/4, self.pos[1]+self.size[1]/4], color=self.color)
			
	def change_state(self):
		self.state = not self.state
	   
	def draw(self):
		screen = self.screen 
		pg.draw.rect(screen.surface, self.color, [*self.get_pos(), *self.size], int(self.stroke))
		if self.state:
			self.checkbox.draw()
		
class InputBox(Rect):
	def __init__(self, pos, size, **styles):
		super().__init__(pos, size, **styles)
		self.textsize = styles.get("textsize", 28)
		self.textcolor = styles.get('textcolor', "white")
		self.textfont = styles.get("textfont", "Arial")
		self.value = ""
		self.overflow = styles.get("overflow", "hidden")
		self.focus = False
		self.stroke = styles.get("stroke", 5)
		self.resolve_styles()
		self._eventname_unfocus = f"inputbox.{self.id}.on.mousedown._desactivate"
		self._eventname_focus = f"inputbox.{self.id}.on.keydown._catch_char"
		self.text = Text(text=self.value, pos=[self.pos[0]+self.size[0]/(self.textsize/2), self.pos[1]+self.size[1]/4], fontsize=self.textsize, color=self.textcolor, fontname=self.textfont)
		# init 
		self.screen.events.add_event(event="mousedown", object=self, callback=self._activate)
		self.screen.events.on_event("mousedown",  self._desactivate, self._eventname_unfocus)
		self.events = {
			"onfocus" :  self._onfocus,
			"unfocus" :  self._unfocus
		} 
		
		
	def _catch_char(self, **kwargs):
		unicode, key = kwargs["unicode"], kwargs["key"]
		if key == 8:
			self.value = self.value[:-1]
			return
		
		if key == 13:
			unicode = ""
		
		self.value += unicode
		if self.overflow == "hidden":
			self._hide_overflow()
			
	def _hide_overflow(self):
		if self.text.size[0] + self.size[0]/(self.textsize/2) > self.size[0]:
			self.value = self.value[:-1]
			self.text.update(text=self.value)
			return self._hide_overflow()
		else:
			return
				
	def _activate(self):
		if self.focus == False:
			self.focus = True    
			self.screen.events.on_event("keydown", self._catch_char, self._eventname_focus)    
			self.events["onfocus"]()    
			self.screen.events.on_event("mousedown", self._desactivate, self._eventname_unfocus)

	def _desactivate(self):
		if self.focus:
			self.focus = False
		self.events["unfocus"]()
		
		self.screen.events.remove_event(self._eventname_focus)
		self.screen.events.remove_event(self._eventname_unfocus)            
		
	def _onfocus(self):
		self.stroke = 1
	def _unfocus(self):
		self.stroke = 5
		
	def onfocus(self, callback):
		self.events["onfocus"] = callback
		self.events["onfocus"]()
		
	def unfocus(self, callback):
		self.events["unfocus"] = callback
		self.events["unfocus"]()       

	def draw(self):
		screen = self.screen
		pg.draw.rect(screen.surface, self.color, [*self.get_pos(), *self.size], int(self.stroke))
		self.text.update(text=self.value)
		self.text.draw()
		
class Button(Rect):
	def __init__(self, pos, size, **styles):
		if "border_radius" in styles:
			self.border_radius = styles["border_radius"]
			del styles["border_radius"]
			
		else:
			self.border_radius = [5] * 4

		super().__init__(pos=pos, size=size, **styles)
		
		if "text" in styles:
			self.text = styles['text']
			self.fontsize = styles.get("fontsize", 28)
			self.textcolor = styles.get('textcolor', "white")
			self.font = styles.get("font", "Arial")
			
		self._eventname = f"button.{self.id}.on.mousedown"
		self.screen.events.add_event(event="mousedown", object=self, callback=lambda: None, name=self._eventname)
		
	def _gen_text_obj(self):
		self.text_obj = Text(text=self.text, pos=[self.pos[0], self.pos[1]], fontsize=self.fontsize, color=self.textcolor, fontname=self.font)
		self.text_obj.pos = [self.pos[0]-self.text_obj.size[0]/2, self.pos[1]-self.text_obj.size[1]/2]

	def onclick(self, callback):
		r'''
		Calls the callback function when the button is clicked
		'''
		self.screen.events.add_event(event="mousedown", object=self, callback=callback, name=self._eventname)
		return self
		
		
	def click(self, func):
		r'''
		<Decorator> Calls the callback function when the button is clicked
		'''
		self.onclick(func)
		return func
	
	def draw(self):
		super().draw()
		if hasattr(self, "text"):
			self._gen_text_obj()
			self.text_obj.draw()
