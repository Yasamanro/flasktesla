class Badge():
	def __init__(self, text):
		self.text = text


class LinearBadgeFactory():
	def __init__(self):
		self.badges = []

	def add_badge(self, limit, badge):
		self.badges.append((limit, badge))


	def get_completed_remaining(self, limit):
		completed, remaining = [], []

		for badge_limit, badge in self.badges:
			if badge_limit <= limit:
				completed.append(badge)
			else:
				remaining.append(badge)

		return completed, remaining



if __name__ == "__main__":
	speed_badge_factory = LinearBadgeFactory()
	bronze_speed_badge = Badge('This is the bronze badge')
	silver_speed_badge = Badge('This is the silver badge')

	speed_badge_factory.add_badge(10, bronze_speed_badge)
	speed_badge_factory.add_badge(20, silver_speed_badge)

	speed = 20  # calculation to get speed record
	badges_for_this_speed = speed_badge_factory.get_badges(speed)

	for badge in badges_for_this_speed:
		print(badge.text)