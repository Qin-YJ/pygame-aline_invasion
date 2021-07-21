class GameStats:
	"""跟踪游戏的统计信息"""
	def __init__(self, ai_game):
		#游戏刚启动时处于活跃状态
		self.game_active = True

		self.settings = ai_game.settings
		self.reset_stats()

	def reset_stats(self):
		self.ships_left = self.settings.ship_limit
		