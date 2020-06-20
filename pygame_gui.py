import sys
import pygame
import cv2
import numpy
class Visualizer:
	def __init__(self,width=640,height=480):
		self.cap = cv2.VideoCapture(0)
		pygame.init()
		self.clock = clock = pygame.time.Clock()
		self.fps = 2400
		self.width = width
		self.height =  height
		self.display = pygame.display
		self.screen = self.display.set_mode((self.width, self.height))
		self.display.set_caption('Visualizer_pygame')
		#self.icon = pygame.image.load('SPCX.ico')
		#self.display.set_icon(self.icon)
		self.running = True
		self.background_colour = (0,0,0)
		self.x,self.y = int(self.width/2),int(self.height/2)
		self.debug = False

		
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				self.cap.release()
				cv2.destroyAllWindows()
				pygame.quit()
				#sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.debug:
					print(pygame.key.name(event.key),"DOWN")
				else:
					pass
			if event.type == pygame.KEYUP:
				if self.debug:
					print(pygame.key.name(event.key),"UP")
				else:
					pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEBUTTONUP:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEMOTION:	
				self.x = event.pos[0]
				self.y = event.pos[1]			
				if self.debug:
					print(event.pos,event.rel,event.buttons)

				else:
					pass
		return self.x,self.y
	def run(self):
		if self.running:
			ret, image = self.cap.read()
			image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
			frame=numpy.rot90(image)
			frame = cv2.flip(frame,0)
			image=pygame.surfarray.make_surface(frame) 
			self.screen.fill(self.background_colour)
			self.screen.blit(image, (0, 0)) 
			color = (255,255,255)
			center = self.x,self.y
			radius = 10
			pygame.draw.circle(self.screen, color, center, radius) 

			#self.display.update()#UPDATE WHOLE SCREEN,IF NO ARGUMENTS GIVEN SAME AS FLIP
			self.display.flip()# UPDATE ENTIRE SCREEN
			self.clock.tick(self.fps)
			#print("FPS:",int(round(self.clock.get_fps())),end="\r")

			
			
#V = Visualizer()
#while V.running:
#	x,y = V.handle_events()
#	print(x,y,end = "\r")
#	V.run()
