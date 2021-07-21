import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
	"""管理游戏资源和行为的类"""

	def __init__(self):
		"""初始化游戏并创建游戏资源"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		
		pygame.display.set_caption("Alien Invasion")

		#创建一个用于存储游戏统计信息的实例
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()#定义精灵组/创建一个编组,Group是对sprite的后缀的处理方法
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#设置背景色
		#self.bg_color = (230,230,230)

	def run_game(self):
		"""开始游戏主循环"""
		while True:
			"""监视键盘和鼠标事件"""
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()


	def _create_fleet(self):
		"""创建外星人群，计算一行可容纳多少个外星人"""
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (4 * alien_width)
		number_alien_x =available_space_x // (2 * alien_width)

		"""计算屏幕可容纳多少行外星人"""
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (5 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)
		#print(number_rows)

		#创建外星人群
		for row_number in range(number_rows):
			for alien_number in range(number_alien_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		"""创建一个外星人并放在当前行"""
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien_height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""有外星人到达边缘时采取相应措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1


	def _fire_bullet(self):
		"""创建一颗子弹，并将其加入到编组bullet中。"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)##将精灵加入组,这是pygame.sprite的特性，add类似append只不过在pygame里用的


	def _check_events(self):
		"""监视键盘和鼠标事件"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				self._check_events_keydown(event)
			elif event.type == pygame.KEYUP:  #检测的是上升沿/下降沿
				self._check_events_keyup(event)
				
	def _check_events_keydown(self,event):
		"""响应按键"""
		if event.key == pygame.K_RIGHT:
		#向右移动飞船
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()		

	def _check_events_keyup(self,event):
		"""响应按键"""
		if event.key == pygame.K_RIGHT:
		#向右移动飞船
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _update_bullets(self):
		self.bullets.update()
					#删除消失的子弹。
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:#别忘了加冒号
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#检查是否有子弹击中了外星人
		collisions = pygame.sprite.groupcollide(
			self.bullets,self.aliens,True,True)
		if not self.aliens:
			#删除现有的子弹并创建一群外星人
			self.bullets.empty()
			self._create_fleet()

	def _check_aliens_bottom(self):
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#像飞船被撞到一样处理
				self._ship_hit()
				break

	def _update_aliens(self):
		self._check_fleet_edges()
		#更新所有外星人的位置
		self.aliens.update()

		#检测外星人和飞船之间的碰撞
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			print("ship hit!!!")
			self._ship_hit()

		#检测是否有外星人到达屏幕底部
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""响应飞船被外星人撞到"""
		#将ships_left减1
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			#清空余下的外星人和子弹
			self.aliens.empty()
			self.bullets.empty()
			#创建一群新的外星人，并将飞船重新放置
			self._create_fleet()
			self.ship.center_ship()
			#暂停
			sleep(0.5)
		else:
			self.stats.game_active = False

	def _update_screen(self):
		"""更新屏幕上的图像，并切换到新屏幕"""

		#每次循环时都重绘屏幕和ship元素
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():#方法.sprites()返回一个列表，其中包含编组bullets中的所有精灵
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#更新整个待显示的Surface对象到屏幕上
		pygame.display.flip()


if __name__ == '__main__':
	#创建游戏实例并运行游戏
	ai = AlienInvasion()
	ai.run_game()