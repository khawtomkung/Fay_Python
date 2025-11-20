
#!/usr/bin/python
# -*- coding: utf8 -*- 

import pygame

class Main:
	
	def __init__(self):
		pygame.init()
		
		self.screenDim = (500,500)
		self.screen = pygame.display.set_mode(self.screenDim)
		self.background = (255,255,255)
		self.running = False
	
	def poll(self):
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				self.running = False
			elif e.type == pygame.KEYUP:
				if e.key == pygame.K_ESCAPE:
					self.running = False
	
	def update(self, dt):
		pass
	
	def draw(self):
		pass
	
	def run(self):
		
		self.running = True
		clock = pygame.time.Clock()
		while self.running:
			dt = clock.tick(40) / 1000.0
			
			self.screen.fill(self.background)
			
			self.poll()
			self.update(dt)
			self.draw()
			
			pygame.display.flip()

if __name__ == '__main__':
	main = Main()
	print ("starting...")
	main.run()
	print ("shuting down...")