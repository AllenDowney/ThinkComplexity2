class TitForTwoTats():
    ''' TitForTat will replicate its opponent's last move. '''
    def step(self, history, round):
        if round == 0:
            action = 1
        elif round == 1:
        	action = 1
        else:
        	#If last two rounds weren't both defections, doesn't defect.
            action = int(history[self.order^1][round - 1] or history[self.order^1][round - 2])
        return action
