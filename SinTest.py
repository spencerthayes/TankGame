import pygame
import math

displayWidth = 640
displayHeight = 480

white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
green = pygame.Color(0,128,0)
red = pygame.Color(255,0,0)

clock = pygame.time.Clock()
FPS = 60

upSprite = pygame.image.load('Up.png')
downSprite = pygame.image.load('Down.png')
rightSprite = pygame.image.load('Right.png')
leftSprite = pygame.image.load('Left.png')

window = pygame.display.set_mode((displayWidth, displayHeight))

def sin(angle):
	return math.sin(math.radians(angle))
	
def cos(angle):
	return math.cos(math.radians(angle))
	
class player(object):
	def __init__(self, startX, startY, angle):
		self.x = startX
		self.y = startY
		self.angle = angle
		self.moving = False
		self.turningClockwise = False
		self.turningCClockwise = False
	
	def draw(self, win):
#		pygame.draw.circle(win, black, (self.x, self.y), 10)
		pygame.draw.line(win, green, (self.x, self.y), (self.x + 20 * cos(self.angle), self.y + 20 * sin(self.angle)))
		if self.angle > 315 or self.angle <= 45:
			spriteRect = rightSprite.get_rect()
			spriteRect.center = self.x, self.y
			window.blit(rightSprite, spriteRect)
					
		elif self.angle > 45 and self.angle <= 135:
			spriteRect = downSprite.get_rect()
			spriteRect.center = self.x, self.y
			window.blit(downSprite, spriteRect)
					
		elif self.angle > 135 and self.angle <= 225:
			spriteRect = leftSprite.get_rect()
			spriteRect.center = self.x, self.y
			window.blit(leftSprite, spriteRect)
					
		elif self.angle > 225 and self.angle <= 315:
			spriteRect = upSprite.get_rect()
			spriteRect.center = self.x, self.y
			window.blit(upSprite, spriteRect)
			
		
		
class projectile(object):
	def __init__(self, x, y, angle, velocity, colour):
		self.x = x
		self.y = y
		self.angle = angle
		self.vel = velocity
		self.colour = colour
		self.visualRadius = 2
		
	def draw(self, win):
		pygame.draw.circle(win, self.colour, (self.x, self.y), self.visualRadius)

gameExit = False

tank = player(50, 50, 0)
bullets = []

def drawFrame():
	window.fill(white)
	tank.draw(window)
	
	for bullet in bullets:
		bullet.draw(window)
	
	pygame.display.update()

while not gameExit:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				tank.turningCClockwise = True
			elif event.key == pygame.K_RIGHT:
				tank.turningClockwise = True
			elif event.key == pygame.K_UP:
				tank.moving = True
			elif event.key == pygame.K_z:
				bulletAngle = tank.angle
				bullets.append(projectile(tank.x, tank.y, tank.angle, 2, red))
			elif event.key == pygame.K_LSHIFT:	
				tank.x += 30 * cos(tank.angle)
				tank.y += 30 * sin(tank.angle)
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				tank.turningCClockwise = False
			elif event.key == pygame.K_RIGHT:
				tank.turningClockwise = False
			elif event.key == pygame.K_UP and tank.moving: 
				tank.moving = False
				
	if tank.moving:
		tank.x += 1 * cos(tank.angle)
		tank.y += 1 * sin(tank.angle)
		
	if tank.turningClockwise:
		tank.angle += 2.5
		if tank.angle == 360:
			tank.angle = 0
		
	if tank.turningCClockwise:
		tank.angle -= 2.5
		if tank.angle < 0:
			tank.angle += 360
		
	for bullet in bullets:
		if bullet.x >= 0 and bullet.x <= displayWidth and bullet.y >= 0 and bullet.y <= displayHeight:
			bullet.x += bullet.vel * cos(bullet.angle)
			bullet.y += bullet.vel * sin(bullet.angle)
		else:
			bullets.pop(bullets.index(bullet))
		
	drawFrame()
	
	clock.tick(FPS)