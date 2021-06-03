import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import math
import pickle
import random

display_fullscreen = True
display_width = False
display_height = False
display_frequency = 80
sound_music = True

try :
	with open(os.getcwd() + "/Settings.conf", "r") as settings_file :
		setting = settings_file.readline()
		while (setting) :
			setting = setting.replace(" ","").lower()
			if (setting[0:10] == "fullscreen") :
				display_fullscreen = (setting[11:14] == "yes")
			elif (setting[0:5] == "width") :
				try :
					display_width = int(setting[6:-1])
				except :
					display_width = False
			elif (setting[0:6] == "height") :
				try :
					display_height = int(setting[7:-1])
				except :
					display_hzight = False
			elif (setting[0:9] == "frequency") :
				try :
					display_frequency = int(setting[10:-1])
				except :
					display_frequency = 80
			elif (setting[0:5] == "music") :
				sound_music = (setting[6:9] == "yes")
			setting = settings_file.readline()
	
except :
	display_fullscreen = True
	display_width = False
	display_height = False
	display_frequency = 80
	sound_music = True
	settings_file = open(os.getcwd() + "/Settings.conf", "w")
	settings_file.write("FULLSCREEN : yes\nWIDTH      : 1920\nHEIGHT     : 1080\nFREQUENCY  : 80\nMUSIC      : yes")
	settings_file.close()

try :
	import cursor
	cursor.hide()
except :
	pass
	
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame_info = pygame.display.Info()


if (display_width == False or display_fullscreen) :
	display_width = pygame_info.current_w
	
	
if (display_height == False or display_fullscreen) :
	display_height = pygame_info.current_h
	
if (display_frequency == False) :
	display_frequency = 80

display_zoom = min(display_width / 480, display_height / 270)
if (display_zoom < 1) :
	display_zoom = 1
display_width = round(480 * display_zoom)
display_height = round(270 * display_zoom)

print("=========================== settings ===========================\n")
print("                fullscreen              " + ["No", "Yes"][display_fullscreen])
print("                window width            " + str(display_width))
print("                window height           " + str(display_height))
print("                frequency               " + str(display_frequency))
print("                music                   " + ["No", "Yes"][sound_music])
print("\n=========================== controls ===========================\n")
print("                [left arrow]            left")
print("                [right arrow]           right")
print("                [space]                 shoot")
print("                [enter]                 restart")
print("                [backspace]             pause")
print("                [escape]                exit")


rocket_angle_accuracy = 2
rocket_size_accuracy = 0.5

try :
	with open(os.getcwd() + "/Data/Resource.bin", "rb") as resource_file:
		resource = pickle.load(resource_file)
	if (display_width != resource[0][0] or display_height != resource[0][1]) :
		error = int("error")
		
except :
	from lxml import etree
	from svg import Rasterizer, Parser
	print("\n======================= sprite generation ======================\n")
	
	def load_svg(path, size, rotation = False) :
		xml = etree.parse(os.getcwd() + "/" + path)
		svg = xml.xpath("//*[@id='svg']")[0]
		background = xml.xpath("//*[@id='background']")[0]
		path_1 = xml.xpath("//*[@id='path-1']")[0]
		path_2 = xml.xpath("//*[@id='path-2']")[0]
		width = int(svg.get("width"))
		height = int(svg.get("height"))
		scale = "scale(" + str((size[0] / width) * display_zoom) +")"
		if (rotation) :
			dimension = max(size[0], size[1]) * 1.4375
			svg.set("width", str(dimension * display_zoom)) 
			svg.set("height", str(dimension * display_zoom)) 
			background.set("width", str(dimension * display_zoom)) 
			background.set("height", str(dimension * display_zoom)) 
			rotate = " rotate(" + str(rotation) + " " + str(width * 0.5) + " " + str(height * 0.5) + ")"
			translate =  " translate(" + str((dimension - size[0]) * 0.5 * display_zoom) + " " + str((dimension - size[1]) * 0.5 * display_zoom) + ")"
			path_1.set("transform", translate + scale) 
			path_2.set("transform", rotate) 
		else :
			svg.set("width", str(size[0] * display_zoom)) 
			svg.set("height", str(size[1]* display_zoom)) 
			background.set("width", str(size[0] * display_zoom)) 
			background.set("height", str(size[1]* display_zoom)) 
			path_1.set("transform", scale) 
		svg = Parser.parse(etree.tostring(xml))
		rasterizer = Rasterizer()
		return (rasterizer.rasterize(svg, svg.width, svg.height), (svg.width, svg.height), "RGBA")
		
	print("[" + 62 * " " + "]", end="\r", flush=True)
	resource = [
		[round(480 * display_zoom), round(270 * display_zoom)],
		[
			load_svg("/Resource/Ship.svg", (24, 16)),
			[
				load_svg("/Resource/Ennemi_0.svg", (24, 16)),
				load_svg("/Resource/Ennemi_1.svg", (24, 16)),
				load_svg("/Resource/Ennemi_2.svg", (24, 16)),
				load_svg("/Resource/Ennemi_3.svg", (24, 16))
			],
			[
			],
			load_svg("/Resource/Shield.svg", (32, 32))
		],
		[
			round(12 * display_zoom),
			round(48 * display_zoom),
		]
	]
	
	sprite_number = (round(360 / rocket_angle_accuracy)) * round((2 * display_zoom) / rocket_size_accuracy) + 6
	sprite_done = 6
	print("[" + round((sprite_done / sprite_number) * 62) * "#" + (62 - round((sprite_done / sprite_number) * 62)) * " " + "]", end="\r", flush=True)

	for angle in range(round(360 / rocket_angle_accuracy)) :
		resource[1][2].append([])
		for taille in range(round((2 * display_zoom) / rocket_size_accuracy)) :
			sprite_done += 1
			resource[1][2][-1].append(load_svg("/Resource/Rocket.svg", (2 + taille * rocket_size_accuracy, 4 + taille * 2 * rocket_size_accuracy), round(360 - (angle * rocket_angle_accuracy))))
		print("[" + round((sprite_done / sprite_number) * 62) * "#" + (62 - round((sprite_done / sprite_number) * 62)) * " " + "]", end="\r", flush=True)
	
	with open(os.getcwd() + "/Data/Resource.bin", "wb") as resource_file :
		pickle.dump(resource, resource_file)
	print("")
		
player_difficulty = 0
modes = ["easy", "medium", "hard"]

print("\n========================== difficulty ==========================\n")
print("                [1]                     " + modes[0])
print("                [2]                     " + modes[1])
print("                [3]                     " + modes[2])

while True :
	try :
		try :
			cursor.show()
		except :
			pass
		player_difficulty = int(input("\n                Select the difficulty : "))
		try :
			cursor.hide()
		except :
			pass
	except :
		player_difficulty = 0
	if (player_difficulty >= 1 and player_difficulty <= 3) :
		player_difficulty -= 1
		print("\n                You launched in " + modes[player_difficulty] + " mode.")
		time.sleep(0.5)
		break
	else :
		print("\n                You failed.")
		time.sleep(0.5)
		
print("\n============================= game =============================\n")

rocket_speed = ([100, 180, 240][player_difficulty] / display_frequency) * display_zoom
rocket_max_damage = 100
rocket_reloading_color = (204, 204, 204)

ship_color = ((40, 154, 204), (20, 77, 102))
ship_life = [500, 250, 100][player_difficulty]
ship_reloading_speed = 12.8/display_frequency
ship_propulsion = (5 / display_frequency) * display_zoom
ship_max_speed = (480 / display_frequency) * display_zoom

ennemi_color = ((204, 52, 40), (102, 26, 20))
ennemi_life = 100
ennemi_reloading_speed = [4.8, 9.6, 14.4][player_difficulty] / display_frequency
ennemi_animation_speed = 1 * display_frequency
ennemi_speed = ([8, 12, 16][player_difficulty] / display_frequency) * display_zoom
ennemi_max_speed = (320 / display_frequency) * display_zoom
ennemi_agressivity = (20,30,30,40,40,40,50,50,50,60,60,60,70,80,100,100)
	
resource[1][0] = pygame.image.frombuffer(*resource[1][0])

for n in range(len(resource[1][1])):
	resource[1][1][n] = pygame.image.frombuffer(*resource[1][1][n])
	
for n_0 in range(len(resource[1][2])):
	for n_1 in range(len(resource[1][2][n_0])):
		resource[1][2][n_0][n_1] = pygame.image.frombuffer(*resource[1][2][n_0][n_1])
		
resource[1][3] = pygame.image.frombuffer(*resource[1][3])
			
pygame.font.init()
resource[2][0] = pygame.font.Font(os.getcwd() + "/Resource/DaysOne.ttf", resource[2][0])
resource[2][1] = pygame.font.Font(os.getcwd() + "/Resource/DaysOne.ttf", resource[2][1])

window = None

if (display_fullscreen) :
	window = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
else :
	window = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(False)
if (sound_music) :
	pygame.mixer.music.load(os.getcwd() + "/Resource/Soundtrack.ogg")
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.play(-1)

sound_ship_shoot = pygame.mixer.Sound(os.getcwd() + "/Resource/Ship_shoot.ogg")
sound_ship_shoot.set_volume(0.3)
sound_ennemi_shoot = pygame.mixer.Sound(os.getcwd() + "/Resource/Ennemi_shoot.ogg")
sound_ennemi_shoot.set_volume(0.4)
sound_ship_hit = pygame.mixer.Sound(os.getcwd() + "/Resource/Ship_hit.ogg")
sound_ship_hit.set_volume(0.4)
sound_ennemi_hit = pygame.mixer.Sound(os.getcwd() + "/Resource/Ennemi_hit.ogg")
sound_ennemi_hit.set_volume(0.4)
sound_ship_shield = pygame.mixer.Sound(os.getcwd() + "/Resource/Ship_shield.ogg")
sound_ship_shield.set_volume(0.4)
sound_ennemi_shield = pygame.mixer.Sound(os.getcwd() + "/Resource/Ennemi_shield.ogg")
sound_ennemi_shield.set_volume(0.4)
sound_rocket_loaded = pygame.mixer.Sound(os.getcwd() + "/Resource/Rocket_loaded.ogg")
sound_rocket_loaded.set_volume(0.5)
sound_win = pygame.mixer.Sound(os.getcwd() + "/Resource/Win.ogg")
sound_win.set_volume(0.5)
sound_lose = pygame.mixer.Sound(os.getcwd() + "/Resource/Lose.ogg")
sound_lose.set_volume(0.5)

class obj():
	data = None
	x = None
	y = None
	speed = None
	angle = None
	image = None
	sprite = None
	colors = None
	rect = None
	second_rect = []
	mask = None
	center = None
	vector = None
	
	def __init__(self, sprite, colors:list = [((0, 1, 0, 1), (255, 255, 255))], position = (0, 0), speed:int = 0, angle:int = 0, data:dict = []):
		super().__setattr__("data", data)
		super().__setattr__("x", position[0])
		super().__setattr__("y", position[1])
		super().__setattr__("speed", speed)
		self.angle = angle
		super().__setattr__("colors", colors)
		self.sprite = sprite
		
	def __setattr__(self, name, value):
		
		if (name == "speed"):
			super().__setattr__("vector", [math.sin((self.angle + 180)/57.295) * value, math.cos((self.angle + 180)/57.295) * value])
			super().__setattr__("speed", value)

		elif (name == "angle"):
			super().__setattr__("vector", [math.sin((value + 180)/57.295) * self.speed, math.cos((value + 180)/57.295) * self.speed])
			super().__setattr__("angle", value)
		elif (name == "sprite"):
			super().__setattr__("mask", pygame.mask.from_threshold(value, (255, 255, 255, 255), (254, 254, 254, 255)))
			super().__setattr__("rect", value.get_rect())
			self.rect.center = (round(self.x), round(self.y))
			super().__setattr__("image", pygame.Surface((self.rect.w, self.rect.h)))
			for color in self.colors :
				surface = pygame.Surface((round((color[0][1] - color[0][0]) * self.rect.w), round((color[0][3] - color[0][2]) * self.rect.h)))
				surface.fill(color[1])
				self.image.blit(surface, (round(color[0][0] * self.rect.w), round(color[0][2] * self.rect.h)))
			self.image.blit(value, (0,0), None, pygame.BLEND_RGBA_MULT)
			super().__setattr__("sprite", value)
		elif (name == "colors"):
			super().__setattr__("image", pygame.Surface((self.rect.w, self.rect.h)))
			for color in value :
				surface = pygame.Surface((round((color[0][1] - color[0][0]) * self.rect.w), round((color[0][3] - color[0][2]) * self.rect.h)))
				surface.fill(color[1])
				self.image.blit(surface, (round(color[0][0] * self.rect.w), round(color[0][2] * self.rect.h)))
			self.image.blit(self.sprite, (0,0), None, pygame.BLEND_RGBA_MULT)
			super().__setattr__("colors", value)
		else :
			super().__setattr__(name, value)
		
	def move(self) :
		self.x = self.x + self.vector[0]
		self.y = self.y + self.vector[1]
		if (self.x < 0) :
			self.x = display_width
		if (self.x > display_width) :
			self.x = 0
		self.rect.center = (round(self.x), round(self.y))
	
	def display(self) :
		self.rect.center = (round(self.x), round(self.y))
		self.second_rect = False
		window.blit(self.image, self.rect, None, pygame.BLEND_RGB_MAX)
		if (self.rect.center[0] <= self.rect.w / 2) :
			self.second_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3])
			self.second_rect.center = (display_width + self.rect.center[0], self.rect.center[1])
			window.blit(self.image, self.second_rect, None, pygame.BLEND_RGB_MAX)
		elif (self.rect.center[0] >= display_width - (self.rect.w / 2)) :
			self.second_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3])
			self.second_rect.center = (0 - display_width + self.rect.center[0], self.rect.center[1])
			window.blit(self.image, self.second_rect, None, pygame.BLEND_RGB_MAX)
		
	def collide(self, object_test) :
		if (self.second_rect and object_test.second_rect) :
			if (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.rect[0], object_test.rect[1] - self.rect[1])) != None) :
				return True
			elif (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.second_rect[0], object_test.rect[1] - self.second_rect[1])) != None) :
				return True
			elif (self.mask.overlap(object_test.mask, (object_test.second_rect[0] - self.rect[0], object_test.second_rect[1] - self.rect[1])) != None) :
				return True
			elif (self.mask.overlap(object_test.mask, (object_test.second_rect[0] - self.second_rect[0], object_test.second_rect[1] - self.second_rect[1])) != None) :
				return True
			else :
				return False
		elif (self.second_rect) :
			if (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.rect[0], object_test.rect[1] - self.rect[1])) != None) :
				return True
			elif (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.second_rect[0], object_test.rect[1] - self.second_rect[1])) != None) :
				return True
			else :
				return False
		elif (object_test.second_rect) :
			if (self.mask.overlap(object_test.mask, (object_test.second_rect[0] - self.rect[0], object_test.second_rect[1] - self.rect[1])) != None) :
				return True
			elif (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.rect[0], object_test.rect[1] - self.rect[1])) != None) :
				return True
			else :
				return False
		else :
			return (self.mask.overlap(object_test.mask, (object_test.rect[0] - self.rect[0], object_test.rect[1] - self.rect[1])) != None)
		
		
def applyForce(previousSpeed, previousAngle, appliedSpeed, appliedAngle) :
	previous_vector = (math.sin(previousAngle/57.295) * previousSpeed, math.cos(previousAngle/57.295) * previousSpeed)
	applied_vector = (math.sin(appliedAngle/57.295) * appliedSpeed, math.cos(appliedAngle/57.295) * appliedSpeed)
	new_vector = (previous_vector[0] + applied_vector[0], previous_vector[1] + applied_vector[1])
	new_speed = math.sqrt(new_vector[0] ** 2 + new_vector[1] ** 2)
	new_angle = 0
	if (new_vector[0] != 0 and new_vector[1] != 0) :
		new_angle = (math.atan(new_vector[0] / new_vector[1]) * 57.295) 
	else :
		if (new_vector[0] > 0):
			new_angle = 270
		elif (new_vector[0] < 0):
			new_angle = 90
		elif (new_vector[1] < 0):
			new_angle = 180
	return new_speed, new_angle
	
def font_render(text, font, position = (0, 0), align = (0, 0), color = (255, 255, 255)):
	rendered_text = font.render(text, True, color)
	w, h = font.size(text)
	x = round(position[0] * display_zoom)
	y = round(position[1] * display_zoom)
	if (align[0] == 1) :
		x -= w / 2
	elif (align[0] == 2) :
		x -= w
	if (align[1] == 1) :
		y -= h / 2
	elif (align[1] == 2) :
		y -= h
	window.blit(rendered_text, (round(x), round(y)))
	
repeat = True
		
while repeat :
	window.fill(0)
	print("                >>> game started")
	
	clock = [
		pygame.time.Clock(),
		time.time()
	]
	
	objects = [
		obj(resource[1][0], [((0, 1, 0, 1), ship_color[0])], (240 * display_zoom, 246 * display_zoom), 0, 270, [ship_life, 0]),
		[],
		[[], []],
		[
		obj(resource[1][3], [((0, 1, 0, 1), ship_color[1])], (0, 0)),
		obj(resource[1][3], [((0, 1, 0, 1), ennemi_color[1])], (0, 0))
		]
	]
	
	keys = [
		False,
		False,
		False
	]
	
	record = None
	try :
		with open(os.getcwd() + "/Data/Record_" + modes[player_difficulty] +".bin", "rb") as record_file:
			record = pickle.load(record_file)
	except :
		record = {
			"score" : 0,
			"combo" : 0,
			"ratio" : [0, 1],
			"time" : "00:00"
		}
		with open(os.getcwd() + "/Data/Record_" + modes[player_difficulty] +".bin", "wb") as record_file :
			pickle.dump(record, record_file)
		
	random.seed(record["score"])
	
	running = True
	repeat = False
	pause = False
	rocket_colision_test = 222 * display_zoom
	rocket_colision_test_distance = 16 * display_zoom
	rocket_out_bottom = 288 * display_zoom
	rocket_out_top = -8 * display_zoom
	rocket_loaded = False
	ennemi_ship_collision = 230 * display_zoom
	ennemi_animation = 0
	ennemi_animation_frame = 0
	ennemi_direction = 90 + round(random.random()) * 180
	player_score = 0
	player_combo = 0
	player_best_combo = 0
	player_precision = [0, 0]

	roles = [*ennemi_agressivity]
	for i in range(16) :
		role = random.choice(roles)
		objects[1].append(obj(resource[1][1][0], [((0, 1, 0, 1), ennemi_color[0])], ((13.5 + 30 * i) * display_zoom, 9.5 * display_zoom), ennemi_speed, ennemi_direction, [ennemi_life, 0, role/100, role/100, [0, 0, 9.5]]))
		roles.remove(role)
	
	while running :
		window.fill(0)
		
		if(ennemi_animation >= ennemi_animation_speed):
			ennemi_animation_frame = (ennemi_animation_frame + 1) % 4
			for ennemi in objects[1] :
				ennemi.sprite = resource[1][1][ennemi_animation_frame]
			ennemi_animation = 0
		else :
			ennemi_animation += 1
		
		events = pygame.event.get()
		for event in events :
			if (event.type == pygame.KEYDOWN) :
				if (event.key == pygame.K_SPACE) :
					rocket_loaded = False
					sound_ship_shoot.stop()
					sound_ship_shoot.play()
					this_rocket_speed, this_rocket_angle = applyForce(rocket_speed, 0, objects[0].speed, objects[0].angle)
					this_rocket_sprite = resource[1][2][round(this_rocket_angle / rocket_angle_accuracy) - 1][round((objects[0].data[1] / rocket_max_damage) * (round(display_zoom / rocket_size_accuracy) - 1))]
					objects[2][0].append(obj(this_rocket_sprite, [((0, 1, 0, 1), ship_color[0])], (objects[0].x, objects[0].y - 8 * display_zoom), this_rocket_speed, this_rocket_angle, [round(objects[0].data[1])]))
					objects[0].data[1] = 0
					objects[0].colors = [((0, 1, 0, 1), ship_color[0]), ((0, 1, 0, 1 - (objects[0].data[0] / ship_life)), ship_color[1])]
					keys[0] = True
				elif (event.key == pygame.K_LEFT) : 
					keys[1] = True
				elif (event.key == pygame.K_RIGHT) : 
					keys[2] = True
				elif (event.key == pygame.K_ESCAPE) : 
					print("                >>> game exited")
					running = False
				elif (event.key == pygame.K_RETURN) : 
					print("                >>> game exited")
					running = False
					repeat = True
				elif (event.key == pygame.K_BACKSPACE) : 
					pause = True
					print("                >>> game paused")
					pause_time = time.time()
					while pause:
						events = pygame.event.get()
						for event in events :
							if (event.type == pygame.KEYDOWN) :
								if (event.key == pygame.K_BACKSPACE):
									pause = False
									print("                >>> game unpaused")
									clock[1] += time.time() - pause_time
								elif (event.key == pygame.K_ESCAPE) :
									print("                >>> game exited")
									pause = False 
									running = False
								elif (event.key == pygame.K_RETURN) :
									print("                >>> game exited")
									pause = False 
									running = False
									repeat = True
			elif (event.type == pygame.KEYUP) :
				if (event.key == pygame.K_SPACE) : 
					keys[0] = False
				elif (event.key == pygame.K_LEFT) : 
					keys[1] = False
				elif (event.key == pygame.K_RIGHT) : 
					keys[2] = False
					
			elif (event.type == pygame.QUIT) :
				running = False
					
		if (keys[0] == False and rocket_loaded == False):
			if (objects[0].data[1] / rocket_max_damage < objects[0].data[0] / ship_life) :
				objects[0].data[1] += ship_reloading_speed * (objects[0].data[0] / ship_life)
				objects[0].colors = [((0, 1, 0, 1), ship_color[0]), ((0, 1, 0, 1 - (objects[0].data[0] / ship_life)), ship_color[1]), ((0, 1, 1 - (objects[0].data[1] / rocket_max_damage), 1), rocket_reloading_color)]
			else :
				rocket_loaded = True
				sound_rocket_loaded.play()
			if (objects[0].data[1] > rocket_max_damage):
				objects[0].data[1] = rocket_max_damage
				objects[0].colors = [((0, 1, 0, 1), ship_color[0]), ((0, 1, 0, 1 - (objects[0].data[0] / ship_life)), ship_color[1]), ((0, 1, 0, 1), rocket_reloading_color)]
		
			
		if (keys[1]) :
			if (objects[0].angle == 270) :
				objects[0].speed -= ship_propulsion
			else :
				objects[0].speed += ship_propulsion
		if (keys[2]) :
			if (objects[0].angle == 270) :
				objects[0].speed += ship_propulsion
			else :
				objects[0].speed -= ship_propulsion
	
		if (objects[0].speed > ship_max_speed) : 
			objects[0].speed = ship_max_speed
		elif (objects[0].speed < ship_propulsion) :
			objects[0].speed = 0
			objects[0].angle = (objects[0].angle + 180) % 360
	
		objects[0].move()
		objects[0].display()
		
		if (keys[0]) :
			objects[3][0].x = objects[0].x
			objects[3][0].y = objects[0].y
			objects[3][0].move()
			objects[3][0].display()
			
		for rocket in objects[2][0] :
			rocket.move()
			if (rocket.y < rocket_out_top):
				objects[2][0].remove(rocket)
			else :
				for ennemi in objects[1] :
					if (ennemi.data[4][0] <= 1) :
						if (abs(ennemi.x - rocket.x) <= rocket_colision_test_distance) :
							if (rocket.collide(ennemi)) :
								sound_ennemi_hit.stop()
								sound_ennemi_hit.play()
								p_vie = ennemi.data[0]
								ennemi.data[0] -= rocket.data[0]
								ennemi.data[3] = 1 - ((1 - ennemi.data[2]) * (ennemi.data[0] / ennemi_life))
								ennemi.colors = [((0, 1, 0, 1), ennemi_color[0]), ((0, 1, 0, 1 - (ennemi.data[0] / ennemi_life)), ennemi_color[1]), ((0, 1, 1 - ennemi.data[1] / rocket_max_damage, 1), rocket_reloading_color)]
								ennemi.data[1] = 0
								if (ennemi.data[0] < 0) :
									ennemi.data[0] = 0
								player_combo += (p_vie - ennemi.data[0])
								if (player_combo > player_best_combo):
									player_best_combo = player_combo
								player_score += player_combo * (((p_vie - ennemi.data[0]) / ennemi_life) ** 2) * 10
								player_precision[0] += p_vie - ennemi.data[0]
								objects[2][0].remove(rocket)
								if (ennemi.data[0] == 0) :
									ennemi_direction = 360 - ennemi_direction
									objects[1].remove(ennemi)
								break
					else :
						objects[3][1].x = ennemi.x
						objects[3][1].y = ennemi.y
						objects[3][1].move()
						if (rocket.collide(objects[3][1])) :
							sound_ennemi_shield.stop()
							sound_ennemi_shield.play()
							objects[2][0].remove(rocket)
				rocket.display()
		
		for rocket in objects[2][1] :
			rocket.move()
			if (rocket.y >= rocket_colision_test):
				if (rocket.y > rocket_out_bottom):
					objects[2][1].remove(rocket)
				if (keys[0]) :
					if (rocket.collide(objects[3][0])) :
						objects[2][1].remove(rocket)
						sound_ship_shield.stop()
						sound_ship_shield.play()
						break
				elif (rocket.collide(objects[0])) :
					sound_ship_hit.stop()
					sound_ship_hit.play()
					objects[2][1].remove(rocket)
					p_vie = objects[0].data[0]
					objects[0].data[0] -= rocket.data[0]
					objects[0].data[1] = 0
					rocket_loaded = False
					if (objects[0].data[0] < 0):
						objects[0].data[0] = 0
					player_precision[1] += p_vie - objects[0].data[0]
					player_combo = 0
					player_comboReload = 0	
					break		
			rocket.display()
				
		for ennemi in objects[1] :
			ennemi.move()
			ennemi.angle = ennemi_direction
			if (ennemi.data[4][0] == 0) :
				ennemi.data[1] += ennemi_reloading_speed * (ennemi.data[0] / ennemi_life)
				if (ennemi.data[1] > rocket_max_damage):
					ennemi.data[1] = rocket_max_damage
				if (ennemi.data[1] / rocket_max_damage >= (ennemi.data[0] / ennemi_life) * ennemi.data[3]) :
					ennemi.data[4][0] = 1
				ennemi.colors = [((0, 1, 0, 1), ennemi_color[0]), ((0, 1, 0, 1 - (ennemi.data[0] / ennemi_life)), ennemi_color[1]), ((0, 1, 1 - ennemi.data[1] / rocket_max_damage, 1), rocket_reloading_color)]
			elif (ennemi.data[4][0] == 2) :
				if (ennemi.y < ennemi.data[4][2] * display_zoom) :
					objects[3][1].x = ennemi.x
					objects[3][1].y = ennemi.y
					objects[3][1].display()
					if (ennemi_direction == 270) :
						ennemi.angle = [225, 240, 247.5][player_difficulty]
					else :
						ennemi.angle = [135, 120, 112.5][player_difficulty]
					ennemi.speed = ennemi_speed * [1.414213562, 1.054092553, 1.030776406][player_difficulty]    
				else :
					ennemi.angle = ennemi_direction
					ennemi.speed = ennemi_speed
					ennemi.data[4][0] = 0
				if (ennemi.y >= ennemi_ship_collision):
					objects[0].data[0] = 0
					player_precision[1] += 1
			else :
				sound_ennemi_shoot.stop()
				sound_ennemi_shoot.play()
				this_rocket_angle = math.atan((objects[0].x - ennemi.x)/(-1 * (objects[0].y - ennemi.y))) * 57.295
				this_rocket_speed, this_rocket_angle = applyForce(rocket_speed, this_rocket_angle, objects[0].speed, objects[0].angle)
				this_rocket_angle = 180 - this_rocket_angle
				this_rocket_sprite = resource[1][2][round(this_rocket_angle / rocket_angle_accuracy) - 1][round((ennemi.data[1] / rocket_max_damage) * (round(display_zoom / rocket_size_accuracy) - 1))]
				objects[2][1].append(obj(this_rocket_sprite, [((0, 1, 0, 1), ennemi_color[0])], (ennemi.x , ennemi.y + 8), this_rocket_speed, this_rocket_angle, [round(ennemi.data[1])]))
				ennemi.data[1] = 0
				objects[3][1].x = ennemi.x
				objects[3][1].y = ennemi.y
				objects[3][1].display()
				ennemi.data[4][0] = 2
				ennemi.data[4][2] += 8
				ennemi.colors = [((0, 1, 0, 1), ennemi_color[0]), ((0, 1, 0, 1 - (ennemi.data[0] / ennemi_life)), ennemi_color[1])]
			ennemi.display()
						
		font_render("Score : " + str(round(player_score)), resource[2][0], (4, 254))
		font_render("Combo : " + str(round(player_combo)), resource[2][0], (148, 254))
		font_render("Life : " + str(math.ceil(objects[0].data[0])), resource[2][0], (292, 254))
		font_render(str(math.floor((player_precision[0]/ennemi_life) * 6.25)) + "%", resource[2][0], (476, 254), (2, 0))
		
		if (objects[0].data[0] <= 0) :
			window.fill(0)
			sound_lose.play()
			print("                >>> game lost")
			font_render("You lose !", resource[2][1], (240, 135), (1, 1), ennemi_color[0])
			font_render("Result :", resource[2][0], (114, 8), (0,0), (0, 184, 32))
			
			font_render("Score", resource[2][0], (114, 28))
			font_render(str(round(player_score)), resource[2][0], (230, 28))
			font_render(str(math.floor(player_score / (13.6 * ennemi_life))) + "%", resource[2][0], (366, 28), (2, 0))
			print("                | score                 " + str(round(player_score)))

			font_render("Best combo", resource[2][0], (114, 48))
			font_render(str(round(player_best_combo)), resource[2][0], (230, 48))
			font_render(str(math.floor(player_best_combo / (ennemi_life * 0.16))) + "%", resource[2][0], (366, 48), (2, 0))
			print("                | best combo            " + str(round(player_best_combo)))
			
			font_render("Ratio", resource[2][0], (114, 68))
			font_render(str(math.floor(player_precision[0])) + ":" + str(math.floor(player_precision[1])), resource[2][0], (230, 68))
			font_render(str(math.floor((player_precision[0] / (player_precision[1] + player_precision[0])) * 100)) + "%", resource[2][0], (366, 68), (2, 0))
			print("                | ratio                 " + str(math.floor(player_precision[0])) + ":" + str(math.floor(player_precision[1])))
			
			game_duration = time.time() - clock[1]
			text_time = str(math.floor(game_duration/60)) 
			if len(text_time) == 1 :
				text_time = "0" + text_time
			text_time = text_time + ":"
			if len(str(math.floor(game_duration % 60))) == 1 :
				text_time =  text_time + "0" + str(math.floor(game_duration % 60))
			else :
				text_time =  text_time + str(math.floor(game_duration % 60))
			font_render("Time", resource[2][0], (114, 88))
			font_render(text_time, resource[2][0], (230, 88))
			font_render("0%", resource[2][0], (366, 88), (2, 0))
			print("                | time                  " + text_time)
			
			font_render("Record :", resource[2][0], (114, 160), (0,0), (0, 184, 32))
			
			font_render("Score", resource[2][0], (114, 180))
			font_render(str(record["score"]), resource[2][0], (230, 180))
			font_render(str(math.floor(record["score"] / (13.6 * ennemi_life))) + "%", resource[2][0], (366, 180), (2, 0))
			
			font_render("Best combo", resource[2][0], (114, 200))
			font_render(str(record["combo"]), resource[2][0], (230, 200))
			font_render(str(math.floor(record["combo"] / (ennemi_life * 0.16))) + "%", resource[2][0], (366, 200), (2, 0))
			
			font_render("Ratio", resource[2][0], (114, 220))
			font_render(str(math.floor(record["ratio"][0])) + ":" + str(math.floor(record["ratio"][1])), resource[2][0], (230, 220))
			font_render(str(math.floor((record["ratio"][0] / (record["ratio"][1] + record["ratio"][0])) * 100)) + "%", resource[2][0], (366, 220), (2, 0))
			
			font_render("Time", resource[2][0], (114, 240))
			font_render(record["time"], resource[2][0], (230, 240))
			record_game_duration = int(record["time"][0:2]) * 60 + int(record["time"][3:5])
			text_percent_record_time = "0%"
			if (record_game_duration >= 125 and record_game_duration < 625):
				text_percent_record_time = str(100 - round((record_game_duration - 125)/5)) + "%"
			font_render(text_percent_record_time, resource[2][0], (366, 240), (2, 0))
			pygame.display.flip()
			
			while running:
				events = pygame.event.get()
				for event in events :
					if (event.type == pygame.QUIT) :
						running = False
					if (event.type == pygame.KEYDOWN) :
						if (event.key == pygame.K_ESCAPE) : 
							running = False
						elif (event.key == pygame.K_RETURN) : 
							running = False
							repeat = True
			
		if (len(objects[1]) == 0) :
			window.fill(0)
			sound_win.play()
			print("                >>> game won")
			font_render("You Win !", resource[2][1], (240, 135), (1, 1), ship_color[0])
			font_render("Result :", resource[2][0], (114, 8), (0,0), (0, 184, 32))
			
			font_render("Score", resource[2][0], (114, 28))
			font_render(str(round(player_score)), resource[2][0], (230, 28))
			font_render(str(math.floor(player_score / (13.6 * ennemi_life))) + "%", resource[2][0], (366, 28), (2, 0))
			print("                | score                 " + str(round(player_score)))
			
			font_render("Best combo", resource[2][0], (114, 48))
			font_render(str(round(player_best_combo)), resource[2][0], (230, 48))
			font_render(str(math.floor(player_best_combo / (ennemi_life * 0.16))) + "%", resource[2][0], (366, 48), (2, 0))
			print("                | best combo            " + str(round(player_best_combo)))
			
			font_render("Ratio", resource[2][0], (114, 68))
			font_render(str(math.floor(player_precision[0])) + ":" + str(math.floor(player_precision[1])), resource[2][0], (230, 68))
			font_render(str(math.floor((player_precision[0] / (player_precision[1] + player_precision[0])) * 100)) + "%", resource[2][0], (366, 68), (2, 0))
			print("                | ratio                 " + str(math.floor(player_precision[0])) + ":" + str(math.floor(player_precision[1])))
			
			game_duration = time.time() - clock[1]
			text_time = str(math.floor(game_duration/60)) 
			if len(text_time) == 1 :
				text_time = "0" + text_time
			text_time = text_time + ":"
			if len(str(math.floor(game_duration % 60))) == 1 :
				text_time =  text_time + "0" + str(math.floor(game_duration % 60))
			else :
				text_time =  text_time + str(math.floor(game_duration % 60))
			font_render("Time", resource[2][0], (114, 88))
			font_render(text_time, resource[2][0], (230, 88))
			percent_text_time = "0%"
			if (game_duration >= 125 and game_duration < 625):
				percent_text_time = str(100 - round((game_duration - 125)/5)) + "%"
			font_render(percent_text_time, resource[2][0], (366, 88), (2, 0))
			print("                | time                  " + text_time)
			
			font_render("Record :", resource[2][0], (114, 160), (0,0), (0, 184, 32))
			
			font_render("Score", resource[2][0], (114, 180))
			font_render(str(record["score"]), resource[2][0], (230, 180))
			font_render(str(math.floor(record["score"]  / (13.6 * ennemi_life))) + "%", resource[2][0], (366, 180), (2, 0))
			
			font_render("Best combo", resource[2][0], (114, 200))
			font_render(str(record["combo"]), resource[2][0], (230, 200))
			font_render(str(math.floor(record["combo"] / (ennemi_life * 0.16))) + "%", resource[2][0], (366, 200), (2, 0))
			
			font_render("Ratio", resource[2][0], (114, 220))
			font_render(str(math.floor(record["ratio"][0])) + ":" + str(math.floor(record["ratio"][1])), resource[2][0], (230, 220))
			font_render(str(math.floor((record["ratio"][0] / (record["ratio"][1] + record["ratio"][0])) * 100)) + "%", resource[2][0], (366, 220), (2, 0))
			
			font_render("Time", resource[2][0], (114, 240))
			font_render(record["time"], resource[2][0], (230, 240))
			record_game_duration = int(record["time"][0:1]) * 60 + int(record["time"][3:4])
			text_percent_record_time = "0%"
			if (record_game_duration >= 125 and record_game_duration < 625):
				text_percent_record_time = str(100 - round((record_game_duration - 125)/5)) + "%"
			font_render(text_percent_record_time, resource[2][0], (366, 240), (2, 0))
				
			new_record = False
			if (player_score > record["score"]) :
				print("                >>> new record")
				new_record = {
					"score" : round(player_score),
					"combo" : round(player_best_combo),
					"ratio" : player_precision,
					"time" : text_time
				}
				with open(os.getcwd() + "/Data/Record_" + modes[player_difficulty] +".bin", "wb") as record_file :
					pickle.dump(new_record, record_file)
				
			pygame.display.flip()
			border = pygame.Surface((round(114 * display_zoom), round(270 * display_zoom)))
			border.fill(0)
			offset = 0
			while running:
				if (new_record):
					window.blit(border, (0, 0))
					window.blit(border, (round(366 * display_zoom), 0))
					for i in range(68) :
						font_render("New record !", resource[2][0], (1, (i-1) * 4 * display_zoom + offset * display_zoom ), (0, 0), (184, 155, 0))
						font_render("New record !", resource[2][0], (479, (i-1) * 4 * display_zoom + offset * display_zoom), (2, 0), (184, 155, 0))
					offset = (offset + 0.2) % 4
					pygame.display.flip()
				events = pygame.event.get()
				for event in events :
					if (event.type == pygame.QUIT) :
						running = False
					if (event.type == pygame.KEYDOWN) :
						if (event.key == pygame.K_ESCAPE) : 
							running = False
						elif (event.key == pygame.K_RETURN) : 
							running = False
							repeat = True
							
		pygame.display.flip()
		clock[0].tick(display_frequency)
		
print("\n============================= exit =============================")
pygame.quit()
input("\n                Press enter to exit.\n")
