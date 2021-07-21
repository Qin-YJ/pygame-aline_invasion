import pygame
from pygame.sprite import Sprite
#彼此之间不用import，因为都是搞到alien_invasion里面运行的

class Bullet(Sprite):
	"""docstring for Bullet"""
	def __init__(self, ai_game): #为创建子弹实例，是需要当前的AlienInvasion实例的，ai_game是在调用Bullet这个类时，括号中需要赋值实例的
		super().__init__()
		self.screen = ai_game.screen#使用时，ai_game.screen是AlienInvasion中的self.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		
		#先在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
		self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
		#将子弹的rect.midtop设置为飞船的rect.midtop，使其看起来是从飞船中射出来的
		self.rect.midtop = ai_game.ship.rect.midtop

		#存储用小数表示的子弹位置
		self.y = float(self.rect.y)

	def update(self):
		#更新表示子弹位置的小数值
		self.y -= self.settings.bullet_speed
		#更新表示子弹的rect位置
		self.rect.y = self.y

	def draw_bullet(self):
		#在屏幕上绘制子弹
		pygame.draw.rect(self.screen,self.color,self.rect)