class suspiciousTitForTat():
    def step(self, history, round):
        if round == 0:
            action = 0
        else:
            # action = history[self.history^1][round-1]
            action = history[self.order^1][round-1]
        return action