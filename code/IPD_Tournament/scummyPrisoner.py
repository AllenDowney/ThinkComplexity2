class scummyPrisoner():
	def step(self, history, rd):
		if len(history[self.order^1][int(len(history[self.order^1]) * .75):]) > 0:
			oppAvg = sum(history[self.order^1][int(len(history[self.order^1]) * .75):]) / len(history[self.order^1][int(len(history[self.order^1]) * .75):]) if rd > 0 else 0
		else:
			oppAvg = 0
		return 0 if oppAvg >= .75 else 1 if (oppAvg < .75 and oppAvg >= .5) else 0