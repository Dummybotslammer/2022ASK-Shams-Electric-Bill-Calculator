import pygame
pygame.init()

class Spritesheet():
	
	#initialiser
	def __init__(self, image):
		self.image = image
		
	#gets the current letter image with the given parameters
	def get_sprite(self, x, y, width, height):
		temp = pygame.Surface((width, height))
		temp.fill((254, 254, 254))
		temp.set_colorkey((254, 254, 254))
		temp.blit(self.image, (0, 0), (x, y, width, height))
		return temp
		
class Font():
	
	#initialiser
	def __init__(self, image, colour_separater, char_order, scale = 1):
		self.load_font(image, colour_separater, char_order, scale)
	
	#loads font	
	def load_font(self, image, colour_separater, char_order, scale):
		self.scale = scale
		self.char_order = char_order
		width = 0
		self.data = []
		x = 0
		for pixel in range(image.get_width()):
			if tuple(image.get_at((pixel, 0))) == colour_separater:
				self.data.append([x, 0, width, image.get_height()])
				x = pixel + 1
				width = 0
				continue
			else:
				width += 1
		self.font_s = Spritesheet(image)
		self.get_chars()
	
	#get data of location of each character image to be used later in the render function	
	def get_chars(self):
		chars = {}
		for index, item in enumerate(self.data):
			char = self.font_s.get_sprite(item[0], item[1], item[2], item[3])
			char = pygame.transform.scale(char, (char.get_width() * self.scale, char.get_height() * self.scale))
			chars[self.char_order[index]] = char
		self.chars = chars
	
	#draws text with the font on a specific surface	
	def render(self, text, pos, screen, offset):
		start_x = pos[0]
		start_y = pos[1]
		for letter in text:
			screen.blit(self.chars[letter], (start_x, start_y))
			start_x += (self.chars[letter].get_width() + offset)
	
	#changes the colour of the font
	def swap_palette(self, old, new):
		temp = pygame.Surface((self.font_s.image.get_width(), self.font_s.image.get_height()))
		temp2 = temp.copy()
		temp2.fill((0, 0, 1))
		temp2.blit(self.font_s.image, (0, 0))
		temp2.set_colorkey(old)
		temp.fill(new)
		temp.blit(temp2, (0, 0))
		temp.set_colorkey((0, 0, 1))
		self.font_s.image = temp.copy()
		self.get_chars()
		
#screen = pygame.display.set_mode((20, 20))
#clock = pygame.time.Clock()
#font = pygame.image.load("/storage/emulated/0/Font.png").convert_alpha()
#display = pygame.Surface((400, 400))
#char_order = "abcdefghijklmnopqrstuvwxyz0123456789?!.,()-+*/<>#[]%='\"{}:;~`¬ @"
#chars = load_font(font, (223, 32, 32, 255), char_order)
#run = True
#while run:
#	display.fill((127, 127, 127))
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			run = False
#	screen.fill((255, 255, 255))
#	render(char_order + "hello world!", (24, 24), display)
#	#for letter in chars:
#		display.blit(chars[letter], (x, 0))
#		x += (chars[letter].get_width() + 1)
#	screen.blit(pygame.transform.scale(display, (2000, 2000)), (0, 0))
#	pygame.display.update()
#pygame.quit()
#	