import random

class Smart():
    ''' Smart will choose to defect or cooperate depending on
    the opponents past moves.
    '''
    def step(self, history, round):
        # Random choice to start
        if (round == 0) or (round == 1):
            action = random.randint(0, 1)
        # If the last three moves are the same, defect
        elif sum(history[not self.order][round-4:round-1])/3 == (1 or 0):
            action = 0
        # Else, do what they did two moves ago
        else:
            action = history[not self.order][round - 2]
        return action