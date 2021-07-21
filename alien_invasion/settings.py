class Settings(object):
	"""存储游戏中的所有设置的类 Settings"""
	def __init__(self):
		#初始化游戏设置
		#屏幕设置
		#super(Settings, self).__init__()
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		
		#飞船设置
		self.ship_speed = 1.5
		self.ship_limit = 3

		#子弹设置
		self.bullet_speed = 2.0
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 4

		#外星人设置
		self.alien_speed = 0.5
		self.fleet_drop_speed = 100
		self.fleet_direction = 1#表示右移
		
