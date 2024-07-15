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
	
class tank(object):
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

player = tank(50, 50, 0)
bullets = []

def drawFrame():
	window.fill(white)
	player.draw(window)
	
	for bullet in bullets:
		bullet.draw(window)
	
	pygame.display.update()

while not gameExit:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.turningCClockwise = True
			elif event.key == pygame.K_RIGHT:
				player.turningClockwise = True
			elif event.key == pygame.K_UP:
				player.moving = True
			elif event.key == pygame.K_z:
				bulletAngle = player.angle
				bullets.append(projectile(player.x, player.y, player.angle, 2, red))
			elif event.key == pygame.K_LSHIFT:	
				player.x += 30 * cos(player.angle)
				player.y += 30 * sin(player.angle)
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player.turningCClockwise = False
			elif event.key == pygame.K_RIGHT:
				player.turningClockwise = False
			elif event.key == pygame.K_UP and player.moving: 
				player.moving = False
				
	if player.moving:
		player.x += 1 * cos(player.angle)
		player.y += 1 * sin(player.angle)
		
	if player.turningClockwise:
		player.angle += 2.5
		if player.angle == 360:
			player.angle = 0
		
	if player.turningCClockwise:
		player.angle -= 2.5
		if player.angle < 0:
			player.angle += 360
		
	for bullet in bullets:
		if bullet.x >= 0 and bullet.x <= displayWidth and bullet.y >= 0 and bullet.y <= displayHeight:
			bullet.x += bullet.vel * cos(bullet.angle)
			bullet.y += bullet.vel * sin(bullet.angle)
		else:
			bullets.pop(bullets.index(bullet))
		
	drawFrame()
	
	clock.tick(FPS)