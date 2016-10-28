import random

class Flipper():
    ''' Flipper will alternate defections and cooperations, selecting the first
        move randomly.
    '''
    def step(self, history, round):
        if round == 0:
            action = random.randint(0, 1)
        else:
            action = history[self.order][round - 1]^1
            # ^ is the bitwise XOR operator, for easy switching from 0 to 1.
        return action